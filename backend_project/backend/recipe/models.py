from datetime import timedelta, datetime
import urllib2

from django.db.models import get_model
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, Count
from django.template.defaultfilters import slugify
from django.utils.timezone import now

from chefs.models import Chefs
from utils import upload_to_random
from utils.images import ImagesFilters


class RecipesManager(models.Manager):
    @classmethod
    def exclude_for_sale(cls, qs):
        """
        Exclude recipes in books for sale from the queryset `qs`
        """
        book_model = get_model('books', 'Book')
        books_for_sale = book_model.objects.filter(book_type=book_model.TO_SELL)
        return qs.exclude(book__pk__in=books_for_sale)

    def explore_header_recipes(self, ):
        return self.explore_recipes().filter(explore_noted=True).order_by('?')

    def explore_recipes(self, chef=None, hide_for_sale=False):
        MIN_PHOTOS = 3

        queryset = self.filter(draft=False, private=False)
        # queryset = queryset.filter(cache_photos__gte=MIN_PHOTOS)

        if chef and not chef.is_anonymous():
            queryset = queryset.exclude(chef__in=chef.following.all())
            queryset = queryset.exclude(pk__in=chef.recipes_added.all())
            queryset = queryset.exclude(chef=chef)  # Don't show own recipes
        queryset = queryset.select_related('chef').order_by('-final_score')

        if hide_for_sale:
            queryset = self.exclude_for_sale(queryset)

        return queryset

    def explore_recipes_pros(self, chef=None):
        queryset = self.explore_recipes(chef)
        queryset = queryset.filter(chef__type=Chefs.TYPE_PRO)
        return queryset

    def explore_recipes_foodies(self, chef=None):
        queryset = self.explore_recipes(chef)
        queryset = queryset.filter(chef__type=Chefs.TYPE_FOODIE)
        return queryset

    def get_recipes_by_book(self, book_id, private=0):
        book_model = get_model('books', 'Book')
        book = book_model.objects.get(pk=book_id)
        if private == 0:
            queryset = book.recipes.filter(draft=0, private=0).select_related('chef').order_by('-final_score')
        else:
            queryset = book.recipes.filter(draft=0).select_related('chef').order_by('-final_score')
        return queryset

    def get_recipes_by_chef(self, chef_id, private=0):
        result = []
        # if limit == -1:
        if private == 0:
            query = '''select * from recipes r1 where (r1.chef_id = %s and r1.draft=0 and r1.private=0) or r1.id in (select r.id from books b, books_has_recipes bhr, recipes r where b.chef_id = %s and b.id = bhr.book_id and r.id = bhr.recipe_id and r.draft = 0 and r.private=0 group by r.id) order by r1.creation_date desc'''
        else:
            query = '''select * from recipes r1 where (r1.chef_id = %s and r1.draft=0) or r1.id in (select r.id from books b, books_has_recipes bhr, recipes r where b.chef_id = %s and b.id = bhr.book_id and r.id = bhr.recipe_id and r.draft = 0 group by r.id) order by r1.creation_date desc'''
        for res in Recipes.objects.raw(query, [chef_id, chef_id]):
            result.append(res)
        return result

    def get_recipes_by_chef_and_name(self, chef_id, name, private=0):
        result = []
        # if limit == -1:
        if private == 0:
            query = '''select * from recipes r1 where (r1.chef_id = %s and r1.name like %s and r1.draft=0 and r1.private=0) or r1.id in (select r.id from books b, books_has_recipes bhr, recipes r where b.chef_id = %s and b.name like %s and b.id = bhr.book_id and r.id = bhr.recipe_id and r.draft = 0 and r.private=0 group by r.id) order by r1.creation_date desc'''
        else:
            query = '''select * from recipes r1 where (r1.chef_id = %s and r1.name like %s and r1.draft=0) or r1.id in (select r.id from books b, books_has_recipes bhr, recipes r where b.chef_id = %s and b.name like %s and b.id = bhr.book_id and r.id = bhr.recipe_id and r.draft = 0 group by r.id) order by r1.creation_date desc'''
        for res in Recipes.objects.raw(query, [chef_id, '%' + name + '%', chef_id, '%' + name + '%']):
            result.append(res)

        return result

    def all_chef_recipes(self, chef, show_draft=False, show_private=False):
        """
        Get all recipes from chef: created by her or copied from other chefs
        If `show_draft` is False do not show recipes created by her that are draft
        If `show_private` is False do not show recipes created by her that are private
        Copied recipes are always filtered with draft=False and private=False
        """
        subfilter = Q(chef=chef)
        if not show_draft:
            subfilter = subfilter & Q(draft=False)
        if not show_private:
            subfilter = subfilter & Q(private=False)
        return self.filter(subfilter |
                           Q(pk__in=chef.recipes_added.all(), draft=False, private=False))

    def search_explore(self, chef, hide_for_sale=False):
        query = self.filter(draft=False, private=False)
        query = query.filter(chef__in=chef.following.all())
        query = query.exclude(pk__in=chef.recipes_added.all())
        query = query.order_by('-creation_date')

        if hide_for_sale:
            query = self.exclude_for_sale(query)
        return query

    def search_new(self, chef=None):
        """
        Not used now. Leave here until new API /1 is finished
        """
        MIN_PHOTOS = 4
        DAYS = 7
        after = now() - timedelta(DAYS)

        query = self.filter(draft=False, private=False)
        query = query.filter(creation_date__gt=after)
        query = query.annotate(num_photos=Count('photos')).filter(num_photos__gte=MIN_PHOTOS)
        query = query.exclude(chef__in=chef.following.all())
        query = query.exclude(pk__in=chef.recipes_added.all())
        query = query.exclude(chef=chef)  # Don't show own recipes
        query = query.order_by('-final_score')
        return query

    def search_updated(self, chef, after, hide_for_sale=False):
        query = self.filter(edit_date__gt=after)
        query = query.filter(Q(chef=chef) |
                             Q(pk__in=chef.recipes_added.all(), draft=False, private=False))
        query = query.order_by('edit_date')

        if hide_for_sale:
            query = self.exclude_for_sale(query)
        return query


class Recipes(models.Model):
    id = models.AutoField(primary_key=True)
    chef = models.ForeignKey(Chefs, blank=True, null=True, related_name="recipes")

    language = models.CharField(max_length=5, blank=True, null=True, choices=settings.LANGUAGES)
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    commensals = models.IntegerField(default=0)
    ingredients_order = models.TextField(blank=True, default="N;")
    serves = models.IntegerField(default=0, blank=True, null=True)
    prep_time = models.IntegerField(default=0, blank=True, null=True)

    draft = models.BooleanField(default=True)
    private = models.BooleanField(default=True)
    noted = models.BooleanField(default=False)
    explore_noted = models.BooleanField(default=False)
    to_sell = models.BooleanField(default=False)

    manual_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    final_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(blank=True, null=True)

    nb_added = models.IntegerField(default=0)
    nb_comments = models.IntegerField(default=0)
    nb_shares = models.IntegerField(default=0)
    nb_likes = models.IntegerField(default=0)

    cache_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    cache_novelty_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    cache_likes = models.IntegerField(default=0)
    cache_likes_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    cache_photo_descriptions = models.IntegerField(default=0)
    cache_photo_descriptions_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    cache_added = models.IntegerField(default=0)
    cache_added_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    cache_photos = models.IntegerField(default=0)
    cache_photos_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.)
    gross_profit = models.IntegerField(max_length=11, null=True, default=75)
    food_cost = models.IntegerField(max_length=11, null=True, default=25)
    vat = models.IntegerField(max_length=11, null=True, default=20)

    recipes = models.ForeignKey('self', blank=True, null=True, related_name="related_recipes")
    ingredients = models.ManyToManyField('Ingredients', through='RecipesHasIngredients')

    cover_image = models.ImageField(upload_to=upload_to_random('recipes/'))

    tags = models.ManyToManyField('Tags', through='RecipesHasTags')
    chefs = models.ManyToManyField(Chefs, through='ChefsHasRecipes', related_name="recipes_added")

    allergens = models.CharField(max_length=200, blank=True)

    objects = RecipesManager()

    class Meta:
        db_table = 'recipes'
        verbose_name_plural = 'recipes'

    def __unicode__(self):
        return self.name

    @property
    def cover(self):
        try:
            if not self.cover_image:
                self.cover_image = self.photos.filter(is_cover=True)[:1][0].image
                self.save()
            return self.cover_image
        except:
            return None

    @property
    def thumb_explore_box(self):
        try:
            if self.cover:
                thumb = thumbnail_url(self.cover, 'explore_box')
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_cover.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_cover.jpg'

    def thumb(self, type):
        try:
            if self.cover:
                thumb = thumbnail_url(self.cover, type)
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_cover.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_cover.jpg'

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def full_url(self):
        if self.draft == 0:
            return reverse('recipe', kwargs={'slug': self.slug, 'id': self.id})
        else:
            return reverse('kitchen_draft', kwargs={'id': self.id})

    @property
    def site_full_url(self):
        site = Site.objects.get_current()
        return site.domain + reverse('recipe', kwargs={'slug': self.slug, 'id': self.id})

    @property
    def is_in_book_for_sale(self):
        """
        Does this recipe belong to a book for sale?
        """
        return self.book_set.filter(book_type=get_model('books', 'Book').TO_SELL).count() > 0

    def book_for_sale(self):
        """
        Return the book for sale the recipe is in, if any.
        If a recipe is in a book for sale it SHOULD NOT be in any other book.
        """
        try:
            return self.book_set.filter(book_type=get_model('books', 'Book').TO_SELL)[0]
        except:
            None

    @property
    def last_comments(self):
        comments_list = []
        for comment in self.comments.all().order_by('-creation_date')[:2]:
            chef = comment.chef
            comments_list.append(dict(chef_name=chef.full_name,
                                      chef_avatar=chef.thumb_chefs_nav_avatar,
                                      comment=comment.comment,
                                      chef_url=chef.site_url))
        return comments_list

    @property
    def public_url(self):
        """
        Recipe public URL. Used in app for share
        """
        return '%s/%s-%i' % (settings.SHARE_URL, self.slug, self.pk)

    def added_by(self, user):
        """
        User has added the recipe
        """
        return ChefsHasRecipes.objects.filter(recipe=self, chef=user).exists()

    def liked_by(self, user):
        """
        User has liked the recipe
        """
        return Likes.objects.filter(recipe=self, chef=user).exists()

    def shared_by(self, user):
        """
        User has shared the recipe
        """
        return Shares.objects.filter(recipe=self, chef=user).exists()

    def reported_by(self, user):
        """
        User has reported the recipe
        """
        return Report.objects.filter(recipe=self, chef=user).exists()

    def commented_by(self, user):
        """
        User has commented the recipe
        """
        return Comments.objects.filter(recipe=self, chef=user).exists()

    def update_adds(self):
        """
        Update cached nb_likes field
        """
        self.nb_added = self.chefs.count()
        self.save()

    def update_likes(self):
        """
        Update cached nb_likes field
        """
        self.nb_likes = self.likes.count()
        self.save()

    def update_shares(self):
        """
        Update cached nb_shares field
        """
        self.nb_shares = self.shares.count()
        self.save()

    def update_comments(self):
        """
        Update cached nb_comments field
        """
        self.nb_comments = self.comments.count()
        self.save()

    def set_ingredients_order(self, ingredients):
        """
        Set `ingredients_order`
        """
        if not ingredients:
            self.ingredients_order = 'N;'
            return
        ingredients_str = []
        for i, ingredient in enumerate(ingredients):
            ingredients_str.append('i:%i' % i)
            ingredients_str.append('i:%i' % ingredient.pk)
        self.ingredients_order = "a:%i:{%s;}" % (len(ingredients), ';'.join(ingredients_str))

    def set_ingredients_order_add(self, ingredient):
        """
        Add ingredient to `ingredients_order`
        """
        default = 'a:1:{i:0;i:%i;}' % ingredient.pk
        if not self.ingredients_order or self.ingredients_order == 'N;':
            self.ingredients_order = default
            return
        try:
            len_ = int(self.ingredients_order.split('{')[0].split(':')[1])
            ingredients = self.ingredients_order.split('{')[1].strip('}')
            self.ingredients_order = 'a:%i:{%si:%i;i:%i;}' % (len_ + 1, ingredients, len_,
                                                              ingredient.pk)
        except:
            self.ingredients_order = default

    def set_ingredients_order_delete(self, ingredient):
        """
        Delete ingredient from `ingredients_order`
        """
        default = 'N;'
        if not self.ingredients_order or self.ingredients_order == 'N;':
            self.ingredients_order = default
            return
        try:
            len_ = int(self.ingredients_order.split('{')[0].split(':')[1])
            if len_ == 1:
                self.ingredients_order = default
                return

            ingredients = self.ingredients_order.split('{')[1].strip('}').strip(';')
            ingredients = [int(i.split(':')[1]) for i in ingredients.split(';')][1::2]
            ingredients.remove(ingredient.pk)

            ingredients_str = []
            for i, pk in enumerate(ingredients):
                ingredients_str.append('i:%i' % i)
                ingredients_str.append('i:%i' % pk)
            self.ingredients_order = "a:%i:{%s;}" % (len(ingredients), ';'.join(ingredients_str))
        except:
            self.ingredients_order = default

    def get_sorted_ingredients_with_linkrecipe(self):
        """
        Get recipe ingredients sorted
        """
        if not self.ingredients_order or self.ingredients_order == 'N;':
            return list(self.ingredients.all())
        try:
            sorted_ingredients = self.ingredients_order.split('{')[1].strip('}').strip(';')
            sorted_ingredients = [int(i.split(':')[1]) for i in sorted_ingredients.split(';')][1::2]
            ingredients_by_pk = {i.pk: i for i in self.ingredients.all()}
            link_recipes_by_ingredient = {i.ingredient_id: i.link_recipe for i in
                                          RecipesHasIngredients.objects.filter(recipe_id=self.id)}
            ret = []
            for pk in sorted_ingredients:
                if pk in ingredients_by_pk:
                    ret += [{'name': ingredients_by_pk[pk], 'linkRecipeId': link_recipes_by_ingredient[pk]}]
            if len(ret) < ingredients_by_pk:
                for pk, ingredient in ingredients_by_pk.iteritems():
                    if pk not in sorted_ingredients:
                        ret += [{'name': ingredient, 'linkRecipeId': link_recipes_by_ingredient}]
            return ret
        except:
            return list(self.ingredients.all())

    def get_sorted_ingredients(self):
        """
        Get recipe ingredients sorted
        """
        if not self.ingredients_order or self.ingredients_order == 'N;':
            return list(self.ingredients.all())
        try:
            sorted_ingredients = self.ingredients_order.split('{')[1].strip('}').strip(';')
            sorted_ingredients = [int(i.split(':')[1]) for i in sorted_ingredients.split(';')][1::2]
            ingredients_by_pk = {i.pk: i for i in self.ingredients.all()}
            ret = []
            for pk in sorted_ingredients:
                if pk in ingredients_by_pk:
                    ret += [ingredients_by_pk[pk]]
            if len(ret) < ingredients_by_pk:
                for pk, ingredient in ingredients_by_pk.iteritems():
                    if pk not in sorted_ingredients:
                        ret += [ingredient]
            return ret
        except:
            return list(self.ingredients.all())

    def save(self, *args, **kwargs):
        self.edit_date = datetime.now()
        super(Recipes, self).save(*args, **kwargs)


class ChefsHasRecipes(models.Model):
    chef = models.ForeignKey(Chefs, db_column="chef_id")
    recipe = models.ForeignKey(Recipes, db_column="recipe_id")

    class Meta:
        db_table = 'chefs_has_recipes'
        unique_together = (("chef", "recipe"),)


class Comments(models.Model):
    recipe = models.ForeignKey(Recipes, blank=True, null=True, related_name="comments")
    chef = models.ForeignKey(Chefs, blank=True, null=True)
    comment = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'


class IngredientsManager(models.Manager):
    def get_or_create(self, ingredients):
        existing = [ingredient for ingredient in self.filter(name__in=ingredients)]
        existing_names = [e.name for e in existing]
        for name in ingredients:
            if name not in existing_names:
                ingredient = self.create(name=name)
                existing += [ingredient]
        return existing


class Ingredients(models.Model):
    name = models.CharField(max_length=200)

    objects = IngredientsManager()

    class Meta:
        db_table = 'ingredients'

    def __unicode__(self):
        return self.name


class RecipesHasIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, db_column="recipe_id")
    ingredient = models.ForeignKey(Ingredients, db_column="ingredient_id")
    link_recipe = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "recipes_has_ingredients"
        unique_together = ('recipe', 'ingredient')


class TagsManager(models.Manager):
    def get_or_create(self, tags):
        existing = [tag for tag in self.filter(name__in=tags)]
        existing_names = [e.name for e in existing]
        for name in tags:
            if name not in existing_names:
                tag = self.create(name=name)
                existing += [tag]
        return existing


class Tags(models.Model):
    name = models.CharField(max_length=200, blank=True, db_index=True)

    objects = TagsManager()

    class Meta:
        db_table = 'tags'
        ordering = ('name',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact", "name__icontains",)


class RecipesHasTags(models.Model):
    recipe = models.ForeignKey(Recipes, db_column="recipe_id")
    tag = models.ForeignKey(Tags, db_column="tag_id")

    class Meta:
        db_table = 'recipes_has_tags'
        unique_together = (('recipe', 'tag'),)
        verbose_name_plural = "recipe's tags"

    def __unicode__(self):
        return u"%s in [%s]-%s" % (self.tag.name, self.recipe.id, self.recipe.name)


class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipes, blank=True, null=True, related_name="likes")
    chef = models.ForeignKey(Chefs, blank=True, null=True, related_name="likes")
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'


class PhotoFilters(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50)
    param1 = models.CharField(max_length=50, blank=True)
    param2 = models.CharField(max_length=50, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'photo_filters'

    def __unicode__(self):
        return self.name

    def apply_to_photo(self, photo):
        if self.type == 'thumbnail':
            return ImagesFilters.thumbnail(photo, int(self.param1), int(self.param2))
        elif self.type == 'relative':
            return ImagesFilters.to_width(photo, int(self.param2))
        else:
            return photo.s3_url


class PhotoStyles(models.Model):
    s3_url = models.ImageField(upload_to=upload_to_random('styles/'), blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    photo = models.ForeignKey('Photos', blank=True, null=True)
    filter = models.ForeignKey(PhotoFilters, blank=True, null=True)

    class Meta:
        db_table = 'photo_styles'
        verbose_name_plural = 'photo styles'


class PhotosManager(models.Manager):
    def latest_updated(self, chef, date):
        """
        Get latest photos updated from chef recipes or chef added recipes
        """
        added_recipes = chef.recipes_added.values_list('id', flat=True)
        return self.filter(Q(recipe__chef=chef) |
                           Q(recipe__in=added_recipes, recipe__draft=False, recipe__private=False)) \
            .filter(edit_date__gt=date) \
            .order_by('edit_date')


class Photos(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, blank=True)
    instructions = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=100, blank=True)
    temperature = models.CharField(max_length=100, blank=True)
    quantity = models.CharField(max_length=100, blank=True)
    is_cover = models.NullBooleanField(default=False)
    photo_order = models.IntegerField(blank=True, null=True)
    image_url = models.ImageField(upload_to=upload_to_random('photos/'))
    s3_url = models.ImageField(upload_to=upload_to_random('photos/'), blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    chef = models.ForeignKey(Chefs, unique=True, blank=True, null=True, related_name="avatar_photos")
    recipe = models.ForeignKey(Recipes, blank=True, null=True, related_name="photos")

    objects = PhotosManager()

    class Meta:
        ordering = ('photo_order',)
        db_table = 'photos'
        verbose_name_plural = 'photos'

    @property
    def image(self):
        if self.image_url is None or self.image_url.name is None or self.image_url.name == '':
            if self.s3_url is not None and self.s3_url.name is not None and self.s3_url.name.startswith('http'):
                # We need to copy the contents of original file to new one used by web
                image_name_split = self.s3_url.name.split('/')
                image_name = image_name_split[len(image_name_split) - 1]

                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urllib2.urlopen(self.s3_url.name).read())
                img_temp.flush()

                self.image_url.save(image_name, File(img_temp))
            else:
                self.image_url = self.s3_url.name

            self.save()
        return self.image_url

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class RecipesFile(models.Model):
    chef = models.ForeignKey(Chefs, blank=True, null=True)
    name = models.CharField(max_length=200)
    file = models.CharField(max_length=255, blank=True)
    realfile = models.CharField(db_column='realFile', max_length=255, blank=True)  # Field name made lowercase.
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        db_table = 'recipes_file'


class Shares(models.Model):
    recipe = models.ForeignKey(Recipes, blank=True, null=True, related_name="shares")
    chef = models.ForeignKey(Chefs, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    via = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'shares'


class Skills(models.Model):
    name = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'skills'


class Report(models.Model):
    recipe = models.ForeignKey(Recipes)
    chef = models.ForeignKey(Chefs)
    subject = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'

# class Edamam(models.Model):
#     request = models.TextField(blank=True)
#     response = models.TextField(blank=True)
#
#     class Meta:
#         db_table = 'edamam'
#
#
# class RecipeHasSubrecipe(models.Model):
#     r_id = models.IntegerField()
#     sr_id = models.IntegerField()
#     sr_price = models.DecimalField(default=0, max_digits=7, decimal_places=2, blank=True)
#     sr_allergens = models.TextField(blank=True)
#     sr_name = models.CharField(max_length=255, blank=True)
#     sr_owner_name = models.CharField(max_length=255, blank=True)
#     order = models.IntegerField(max_length=8, default=0)
#     amount = models.CharField(max_length=255,blank=True)
#     class Meta:
#         db_table = 'recipe_has_subrecipe'
#
#
# class RecipeHasIngredient(models.Model):
#     recipe_id = models.IntegerField()
#     text = models.TextField(blank=True)
#     custom_ingredient_id = models.IntegerField(blank=True)
#     generic_ingredient_id = models.IntegerField(blank=True)
#     measure = models.CharField(max_length=255, blank=True)
#     quantity = models.DecimalField(max_digits=11, decimal_places=3, default=0)
#     weight_in_gr = models.DecimalField(max_digits=14, decimal_places=3, default=0)
#     price = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
#     allergens = models.TextField(blank=True)
#     ingredient_name = models.CharField(max_length=255, blank=True)
#     order = models.IntegerField(max_length=8, default=0)
#
#     class Meta:
#         db_table = 'recipe_has_ingredient'
