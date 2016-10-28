from django.db import models
from model_utils.models import TimeStampedModel


class Banner(TimeStampedModel):

    BANNER_TYPE_BANNER = 1
    BANNER_TYPE_CATEGORY = 2
    BANNER_TYPE_PRODUCT = 3
    BANNER_TYPE_COLLECTION = 4

    BANNER_TYPES = (
        (BANNER_TYPE_BANNER, 'Banner'),
        (BANNER_TYPE_CATEGORY, 'Category'),
        (BANNER_TYPE_PRODUCT, 'Product'),
        (BANNER_TYPE_COLLECTION, 'Collection')
    )
    title = models.CharField(max_length=128, blank=True, null=True)
    subtitle = models.CharField(max_length=128, blank=True, null=True)
    text = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField('image', upload_to='banners/')
    is_active = models.BooleanField(default=False)
    url = models.CharField(max_length=1024, blank=True, null=True)
    type = models.IntegerField(choices=BANNER_TYPES, default=BANNER_TYPE_BANNER)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'banners'
