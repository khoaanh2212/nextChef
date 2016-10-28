from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from .models import Product, ProductImage


class ProductPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_photo_thumb')

    class Meta:
        model = ProductImage
        fields = ('id', 'photo', 'description', 'order')

    def get_photo_thumb(self, obj):
        return thumbnail_url(obj.photo, 'product_app_thumb')


class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'shop_url', 'shop_title', 'photos')
