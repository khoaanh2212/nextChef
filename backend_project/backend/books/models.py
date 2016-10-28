from django.conf import settings
from django.db import connection, models
from django.db.models import Sum, Q
from django.template.defaultfilters import slugify
from django.utils.timezone import now

from chefs.models import Chefs
from recipe.models import Recipes, Photos, ChefsHasRecipes
from utils import upload_to_random


class BookManager(models.Manager):
    def all_books(self, chef, show_private=False, show_for_sale=True):
        copied_books = chef.books_added.all()
        query = self.filter(Q(chef=chef) | Q(pk__in=copied_books))
        if not show_private:
            query = query.exclude(book_type=Book.PRIVATE)
            query = query.exclude(private=True)
            query = query.exclude(status__in=(Book.DRAFT, Book.UNAVAILABLE))
        if show_for_sale is False:
            query = query.exclude(book_type=Book.TO_SELL)
        else:
            query = query.extra(select={'for_sale': "book_type = '%s'" % Book.TO_SELL})
            query = query.order_by('-for_sale', 'name', 'id')
        return query

    def all_books_to_sell(self):
        return self.filter(status=Book.AVAILABLE, book_type=Book.TO_SELL)

    def _search_books(self, chef):
        query = self.filter(book_type=Book.TO_SELL)
        query = query.exclude(status__in=(Book.DRAFT, Book.UNAVAILABLE))
        if not chef.is_anonymous():
            query = query.exclude(chef=chef)
            query = query.exclude(pk__in=chef.books_added.all())
        query = query.extra(select={'for_sale': "book_type = '%s'" % Book.TO_SELL})
        query = query.order_by('-for_sale', '-creation_date', 'id')
        return query

    def explore(self, chef):
        query = self._search_books(chef)
        query = query.filter(chef__in=chef.following.all())
        return query

    def recommended(self, chef):
        query = self._search_books(chef)
        if not chef.is_anonymous():
            query = query.exclude(chef__in=chef.following.all())
        return query


class Book(models.Model):
    NORMAL = 'N'
    TO_SELL = 'S'
    PRIVATE = 'P'
    TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (TO_SELL, 'To sell'),
        (PRIVATE, 'Private'))
    DRAFT = 'D'
    AVAILABLE = 'A'
    UNAVAILABLE = 'U'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'))

    name = models.CharField(max_length=200)
    book_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=NORMAL)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=AVAILABLE)
    language = models.CharField(max_length=5, blank=True, choices=settings.LANGUAGES)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    product_id = models.CharField(max_length=255, blank=True)  # Apple product ID
    score = models.IntegerField(default=0)
    added = models.BooleanField(default=False)
    private = models.BooleanField(default=True)

    # This should be name 'cover' but there is already a 'property' named 'cover'
    image = models.FileField(upload_to=upload_to_random('books/covers/'), blank=True, null=True)
    video_app = models.FileField(upload_to=upload_to_random('books/videos/'), blank=True, null=True)
    video_web = models.FileField(upload_to=upload_to_random('books/videos/'), blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    nb_shares = models.IntegerField(default=0)
    nb_comments = models.IntegerField(default=0)
    nb_added = models.IntegerField(default=0)

    chef = models.ForeignKey(Chefs, blank=True, null=True, related_name='books')
    chefs = models.ManyToManyField(Chefs, through='ChefsHasBooks', related_name="books_added")
    recipes = models.ManyToManyField(Recipes, through='BookHasRecipes')

    collaborators = models.TextField(blank=True)

    objects = BookManager()

    class Meta:
        db_table = 'books'

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def cover(self):
        recipes = self.recipes.all()[:1]
        if recipes.count() > 0:
            return recipes[0].cover
        else:
            return None

    @property
    def recipes_total(self):
        return self.recipes.count()

    @property
    def likes_total(self):
        likes = self.recipes.all().aggregate(Sum('nb_likes'))
        result = likes.get('nb_likes__sum', 0)
        return result if result else 0

    @property
    def recipes_public(self):
        return self.recipes.all().filter(draft=0, private=0).count()

    def add_recipe(self, recipe):
        """
        Add recipe to book
        """
        try:
            BookHasRecipes.objects.create(book=self, recipe=recipe)
        except:
            pass

    def has_recipe(self, recipe):
        """
        Add recipe to book
        """
        try:
            return BookHasRecipes.objects.filter(book=self, recipe=recipe).count() > 0
        except:
            return False

    def delete_recipe(self, recipe):
        try:
            BookHasRecipes.objects.filter(book=self, recipe=recipe).delete()
        except:
            pass

    def added_by(self, user):
        """
        User has added the book
        """
        return ChefsHasBooks.objects.filter(book=self, chef=user).exists()

    def public_recipes(self, chef, show_private=False):
        """
        Get all recipes from the book that are not draft and are not private
        If `show_private` show also private recipes if they are from the chef
        """
        query = self.recipes.filter(draft=False)
        if show_private:
            query = query.filter(Q(chef=chef) | Q(private=False) | Q(private=True))
        else:
            query = query.filter(private=False)
        return query

    def photos(self, chef, show_private=False):
        """
        Get all photos from the public recipes of the book
        """
        recipes = self.public_recipes(chef, show_private).values_list('id', flat=True)
        return Photos.objects.filter(recipe__in=recipes)

    @property
    def most_popular_recipe_cover_image(self):
        try:
            photos = Photos.objects\
                .filter(is_cover=True)\
                .filter(recipe__in=self.recipes.all(), recipe__draft=False, recipe__private=False)\
                .order_by('-recipe__nb_likes')
            return photos[0]
        except:
            return None

    @property
    def is_public(self):
        """
        The book is intended to be seen for other users othen than the creator
        """
        return self.book_type != self.PRIVATE and self.status == self.AVAILABLE

    @property
    def can_be_sold(self):
        """
        Book is available for sale
        """
        return self.book_type == self.TO_SELL and self.status == self.AVAILABLE

    def user_has_bought_it(self, user):
        """
        Chef has bought the book (or chef is the book's chef)
        """
        return self.chef == user or ChefsHasBooks.objects.filter(book=self, chef=user).exists()

    def buy(self, user, vendor, transaction_id):
        """
        Create the book sale transaction
        """
        ChefsHasBooks.objects.create(chef=user, book=self)
        for recipe in self.recipes.filter(draft=False, private=False):
            ChefsHasRecipes.objects.create(chef=user, recipe=recipe)
        return BookSale.create_sale(book=self, chef=user, price=self.price, vendor=vendor,
                                    transaction_id=transaction_id)


class BookHasRecipes(models.Model):
    book = models.ForeignKey(Book, db_column='book_id')
    recipe = models.ForeignKey(Recipes, db_column='recipe_id')

    class Meta:
        db_table = 'books_has_recipes'
        unique_together = (("book", "recipe"),)


class ChefsHasBooks(models.Model):
    chef = models.ForeignKey(Chefs, db_column="chef_id")
    book = models.ForeignKey(Book, db_column='book_id')

    class Meta:
        db_table = 'chefs_has_books'
        unique_together = (("chef", "book"),)


class BookSale(models.Model):
    SALE = 'S'

    GOOGLE = 'G'
    APPLE = 'A'
    STRIPE = 'S'

    VENDOR_CHOICES = (
        (GOOGLE, 'Google'),
        (APPLE, 'Apple'),
        (STRIPE, 'Stripe'))

    chef = models.ForeignKey(Chefs)
    book = models.ForeignKey(Book)
    sale_date = models.DateTimeField()
    price = models.FloatField()
    relation_type = models.CharField(max_length=1, default=SALE)
    vendor = models.CharField(max_length=1, choices=VENDOR_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)

    @classmethod
    def create_sale(cls, book, chef, price, vendor, transaction_id):
        sale = cls(book=book, chef=chef, sale_date=now(), price=price, vendor=vendor)
        sale.transaction_id = "%s-%s" % (vendor, transaction_id)
        sale.save()
        return sale

    @classmethod
    def transaction_exists(cls, vendor, transaction):
        transaction_id = "%s-%s" % (vendor, transaction)
        return cls.objects.filter(transaction_id=transaction_id).exists()
