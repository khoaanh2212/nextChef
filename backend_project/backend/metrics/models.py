from django.db import models
from django.utils.translation import ugettext_lazy as _


class Metric(models.Model):
    """
    This entity holds custom metrics.
    """
    # KPI codes
    KPI_REGISTERED_USERS = 'registered_users'
    KPI_TOTAL_USERS = 'total_users'
    KPI_TOTAL_RECIPES = 'total_recipes'
    KPI_TOTAL_RECIPES_3_PHOTOS = 'total_recipes_3_photos'
    KPI_TOTAL_FOLLOWS = 'total_follows'
    KPI_TOTAL_LIKES = 'total_likes'
    KPI_TOTAL_COMMENTS = 'total_comments'
    KPI_SUPERACTIVE_USERS = 'superactive_users'
    KPI_ACTIVE_USERS = 'active_users'
    KPI_SLEEPING_USERS = 'sleeping_users'
    KPI_DEAD_USERS = 'dead_users'

    # Segment codes
    SEG_FOODIES = 'foodies'
    SEG_CHEFS = 'pros'
    SEG_ALL = 'all'

    kpi = models.CharField(max_length=30)
    segment = models.CharField(_('Segment'), max_length=255, null=True, blank=True)
    value_num = models.IntegerField(default=0)
    value_str = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateField()

    class Meta:
        verbose_name = _('metric')
        ordering = ('kpi', 'created')
        db_table = 'metrics'
        unique_together = ('created', 'kpi', 'segment')

    def __unicode__(self):
        return "%s-%s: %d" % (self.kpi, self.created, self.value_num)

    @classmethod
    def insert_metric(cls, kpi_code, date_created, value, value_str=None, segment=None):
        m = Metric()
        m.kpi = kpi_code
        m.created = date_created
        m.segment = segment
        m.value_num = value
        m.value_str = value_str
        m.save()
