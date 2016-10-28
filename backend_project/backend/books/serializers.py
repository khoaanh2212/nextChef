from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from api_utils.fields import IntegerBooleanField
from api_utils.pagination import CookboothPaginationSerializer
from api_utils.serializers import CookboothModelSerializer
from chefs.serializers import embeded_chef_serializer, APIV1EmbedChefSerializer

from django.conf import settings
from .models import Book, BookSale
from django.core.urlresolvers import reverse


class WebBookSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    chef_full_name = serializers.SerializerMethodField('get_chef_full_name')
    nb_recipes = serializers.Field('recipes_total')
    url = serializers.SerializerMethodField('get_book_url')

    class Meta:
        model = Book
        fields = ('id', 'chef' ,'name', 'nb_recipes', 'book_type', 'price', 'image_url', 'chef_full_name',
                  'url', 'private','collaborators')

    def get_image_url(self, obj):
        try:
            if obj.image != None:
                return thumbnail_url(obj.image, 'explore_box')
            else:
                return thumbnail_url(obj.most_popular_recipe_cover_image.image_url, 'recipe_step')
        except:
            return settings.STATIC_URL + 'img/chef_cover.jpg'

    def get_chef_full_name(self, obj):
        return obj.chef.get_full_name()

    def get_book_url(self, obj):
        return reverse('book', kwargs={'id': obj.id})


class WebBookSerializerPublic(serializers.ModelSerializer):
    # nb_recipes is count of non-draft and non-private recipes

    nb_recipes = serializers.Field('recipes_public')

    class Meta:
        model = Book
        fields = ('id', 'name', 'nb_recipes')


class ApiBookSerializer(CookboothModelSerializer):
    added = serializers.SerializerMethodField('has_added')
    most_popular_recipe_cover_image = serializers.SerializerMethodField('get_popular_cover')

    class Meta:
        model = Book
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'added', 'book_type',
                  'price', 'product_id', 'status', 'nb_added', 'nb_shares', 'nb_comments',
                  'most_popular_recipe_cover_image')

        read_only_fields = ('chef', 'edit_date', 'creation_date', 'book_type', 'status',
                            'nb_added', 'nb_shares', 'nb_comments', 'price', 'product_id')

    def get_popular_cover(self, obj):
        if not self.context.get('most_popular_recipe_cover_image') is True:
            return None
        photo = obj.most_popular_recipe_cover_image
        if photo:
            if 'http' in photo.s3_url.name:
                photo_url = photo.s3_url.name
            else:
                photo_url = photo.s3_url.url

            return {
                'id': photo.pk,
                'url': photo_url,
                'creation_date': self.datetime_to_timestamp(photo.creation_date),
                'edit_date': self.datetime_to_timestamp(photo.edit_date),
            }
        else:
            return None

    def has_added(self, obj):
        return obj.added_by(self.user)

    def transform_chef(self, obj, value):
        return embeded_chef_serializer(obj.chef)

    def save_object(self, obj, **kwargs):
        obj.chef = self.user
        super(ApiBookSerializer, self).save_object(obj, **kwargs)

    def to_native(self, obj):
        ret = super(ApiBookSerializer, self).to_native(obj)
        if not ret.get('most_popular_recipe_cover_image'):
            ret.pop('most_popular_recipe_cover_image', None)
        return ret


class ApiBookPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'books'


class ApiBookSpecialSerializer(ApiBookSerializer):
    """
    Special readonly serializer used in /{0,1}/chef/:chef_id/books
    """
    nb_likes = serializers.SerializerMethodField('get_nb_likes')
    nb_recipes = serializers.SerializerMethodField('get_nb_recipes')

    def get_nb_likes(self, obj):
        return obj.likes_total

    def get_nb_recipes(self, obj):
        count_private = obj.chef == self.context[u'request'].user
        cnt = obj.public_recipes(obj.chef, count_private).count()
        return cnt if cnt else 0

    class Meta:
        model = Book
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'added', 'nb_likes', 'price',
                  'product_id', 'nb_recipes', 'most_popular_recipe_cover_image', 'book_type',
                  'status')


class ApiBookMinimalSerializer(CookboothModelSerializer):
    """
    Serializer with minimal information about a book
    """
    nb_recipes = serializers.Field('recipes_public')
    cover = serializers.SerializerMethodField('get_cover')

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'product_id', 'cover', 'nb_recipes')

    def get_nb_recipes(self, obj):
        count_private = obj.chef == self.context[u'request'].user
        cnt = obj.public_recipes(obj.chef, count_private).count()
        return cnt if cnt else 0

    def get_cover(self, obj):
        if obj.image:
            return obj.image.url

        photo = obj.most_popular_recipe_cover_image
        if not photo:
            return None
        return photo.s3_url.name if photo.s3_url.name.startswith('http') else photo.s3_url.url


class ApiV1BookSerializer(CookboothModelSerializer):
    """
    Readonly serializer used in v1 to show a book
    """
    added = serializers.SerializerMethodField('has_added')
    cover = serializers.SerializerMethodField('get_cover')
    chef = APIV1EmbedChefSerializer(many=False, read_only=True)
    recipes = serializers.SerializerMethodField('get_recipes')

    class Meta:
        model = Book
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'book_type', 'description',
                  'price', 'product_id', 'video_app', 'video_web', 'nb_added', 'nb_shares',
                  'nb_comments', 'added', 'cover', 'recipes')

    def transform_video_app(self, obj, value):
        return obj.video_app.url if obj.video_app else None

    def transform_video_web(self, obj, value):
        return obj.video_web.url if obj.video_web else None

    def has_added(self, obj):
        return obj.added_by(self.user)

    def get_cover(self, obj):
        if obj.image:
            return obj.image.url

        photo = obj.most_popular_recipe_cover_image
        if not photo:
            return None
        return photo.s3_url.name if photo.s3_url.name.startswith('http') else photo.s3_url.url

    def get_recipes(self, obj):

        show_private = False
        if self.user == obj.chef:
            show_private = True
        elif self.user != obj.chef:
            chef_id = Book.objects.filter(pk=obj.id).values_list('chef', flat=True)
            other_chef_ids = Book.objects.filter(pk=obj.id)[0].chefs.all().values_list('id', flat=True)
            if self.user.id in other_chef_ids:
                show_private = True

        recipes = obj.public_recipes(self.user, show_private)
        return [
            {'id': r.pk, 'name': r.name, 'url': r.public_url, 'description': r.description}
            for r in recipes
            ]


class ApiV1ExploreBookSerializer(CookboothModelSerializer):
    """
    Readonly serializer used in v1 to show a book in the 'explore' endpoints
    Also used in /1/books/for-sale
    """
    nb_recipes = serializers.Field('recipes_public')
    cover = serializers.SerializerMethodField('get_cover')
    url = serializers.SerializerMethodField('get_url')
    chef = APIV1EmbedChefSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'book_type', 'description',
                  'price', 'score', 'nb_added', 'nb_shares', 'nb_comments', 'cover', 'video_app',
                  'video_web', 'product_id', 'nb_recipes', 'url',)

    def transform_video_app(self, obj, value):
        return obj.video_app.url if obj.video_app else None

    def transform_video_web(self, obj, value):
        return obj.video_web.url if obj.video_web else None

    def get_cover(self, obj):
        if obj.image:
            return obj.image.url

        photo = obj.most_popular_recipe_cover_image
        if not photo:
            return None
        return photo.s3_url.name if photo.s3_url.name.startswith('http') else photo.s3_url.url

    def get_url(self, obj):
        return reverse('book', kwargs={'id': obj.id})


class ApiBookBuySerializer(serializers.Serializer):
    """
    Serializer to validate the buy book endpoint
    """
    vendor = serializers.CharField(max_length=1)
    transaction = serializers.CharField(max_length=98)

    def validate_vendor(self, attrs, source):
        if attrs.get(source) not in (BookSale.APPLE, BookSale.GOOGLE):
            raise serializers.ValidationError("Invalid vendor")
        return attrs

    def validate(self, data):
        if BookSale.transaction_exists(data['vendor'], data['transaction']):
            raise serializers.ValidationError("Transaction already exists")
        return data
