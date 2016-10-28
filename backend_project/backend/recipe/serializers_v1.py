from rest_framework import serializers

from api_utils.pagination import CookboothPaginationSerializer
from api_utils.serializers import CookboothModelSerializer
from books.serializers import ApiV1ExploreBookSerializer
from chefs.serializers import (
    APIV1EmbedChefSerializer, APIV1ChefsSerializer, embeded_chef_serializer)
from products.serializers import ProductSerializer

from .models import Comments, Photos, Recipes


class APIV1CommentsSerializer(CookboothModelSerializer):
    chef = APIV1EmbedChefSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'chef', 'comment')
        read_only_fields = ('comment',)


class APIV1PhotoSerializer(CookboothModelSerializer):
    class Meta:
        model = Photos
        fields = ('id', 'instructions', 'image_url', 'photo_order')


class APIV1RecipesSerializer(CookboothModelSerializer):
    image_url = serializers.Field('thumb_explore_box')
    url = serializers.Field('full_url')
    public_url = serializers.Field('public_url')
    last_comments = serializers.Field('last_comments')
    description = serializers.Field('description')
    chef = APIV1ChefsSerializer(many=False, read_only=True)
    comments = APIV1CommentsSerializer(many=True)
    photos = APIV1PhotoSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    ingredients = serializers.WritableField(required=False)
    tags = serializers.WritableField(required=False)

    nb_added = serializers.Field('cache_added')
    added = serializers.SerializerMethodField('has_added')
    shared = serializers.SerializerMethodField('has_shared')
    commented = serializers.SerializerMethodField('has_commented')

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'url', 'public_url', 'description', 'serves', 'prep_time', 'creation_date',
                  'edit_date', 'chef', 'image_url', 'comments', 'tags', 'products', 'ingredients', 'to_sell',
                  'photos', 'nb_likes', 'nb_added', 'nb_shares', 'nb_comments', 'added', 'shared',
                  'commented', 'last_comments')

    def has_added(self, obj):
        return obj.added_by(self.user)

    def has_shared(self, obj):
        return obj.shared_by(self.user)

    def has_commented(self, obj):
        return obj.commented_by(self.user)

    def transform_ingredients(self, obj, value):
        return [{'id': i.pk, 'name': i.name} for i in obj.get_sorted_ingredients()]

    def transform_tags(self, obj, value):
        return [{'id': t.pk, 'name': t.name} for t in obj.tags.all()]

    def get_date(self, obj):
        #return datetime_to_timestamp(obj)
        obj.isoformat() if hasattr(obj, 'isoformat') else obj


class APIV1EmbedRecipesSerializer(CookboothModelSerializer):
    image_url = serializers.Field('thumb_explore_box')
    url = serializers.Field('full_url')
    public_url = serializers.Field('public_url')

    chef = APIV1EmbedChefSerializer(many=False, read_only=True)

    added = serializers.SerializerMethodField('has_added')
    shared = serializers.SerializerMethodField('has_shared')
    commented = serializers.SerializerMethodField('has_commented')

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'url', 'public_url', 'chef', 'image_url', 'nb_likes', 'nb_added',
                  'nb_shares', 'nb_comments', 'added', 'shared', 'commented')

    def has_added(self, obj):
        return obj.added_by(self.context['request'].user)

    def has_shared(self, obj):
        return obj.shared_by(self.context['request'].user)

    def has_commented(self, obj):
        return obj.commented_by(self.context['request'].user)


class ApiV1ExploreRecipeSerializer(CookboothModelSerializer):
    image_url = serializers.Field('thumb_explore_box')
    url = serializers.Field('full_url')
    public_url = serializers.Field('public_url')

    chef = APIV1ChefsSerializer(many=False, read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'url', 'public_url', 'creation_date', 'edit_date', 'chef',
                  'image_url', 'to_sell', 'nb_likes', 'nb_added', 'nb_shares', 'nb_comments')


class ApiV1RecommendPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'recipes'

    def get_books(self, page):
        books_per_page = self.context['items_per_page']['books']
        start = page * books_per_page
        books = self.context['books'][start:start + books_per_page]
        return [ApiV1ExploreBookSerializer(b).data for b in books]

    def get_chefs(self, page):
        chefs_per_page = self.context['items_per_page']['chefs']
        start = page * chefs_per_page
        chefs = self.context['chefs'][start:start + chefs_per_page]
        return [APIV1ChefsSerializer(c).data for c in chefs]

    def get_colls(self, page):
        from colls.serializers import CollsRecommendSerializer  # Circular dependency

        colls_per_page = self.context['items_per_page']['colls']
        start = page * colls_per_page
        pks = self.context['colls_pks'][start:start + colls_per_page]
        colls = self.context['colls'].filter(pk__in=pks)
        return [CollsRecommendSerializer(c).data for c in colls]

    def get_noted(self, page):
        noted_per_page = self.context['items_per_page']['noted']
        start = page * noted_per_page
        pks = self.context['noted_pks'][start:start + noted_per_page]
        noted = self.context['noted'].filter(pk__in=pks)
        return [ApiV1ExploreRecipeSerializer(n).data for n in noted]

    def to_native(self, obj):
        ret = super(ApiV1RecommendPaginatedSerializer, self).to_native(obj)
        current_page = self.object.number - 1
        ret['books'] = self.get_books(current_page)
        ret['chefs'] = self.get_chefs(current_page)
        ret['colls'] = self.get_colls(current_page)
        ret['noted'] = self.get_noted(current_page)
        return ret
