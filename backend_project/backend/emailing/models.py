import datetime
from django.db import models
from django.utils.timezone import utc
from chefs.models import Chefs
from pysendy import Sendy
from django.conf import settings

class EmailingListManager(models.Manager):
    
    def subscribe_chef(self, chef):
        
        s = Sendy(base_url=settings.SENDY_URL)
        
        lists = EmailingList.objects.all()
        for list in lists:
            if list.check_match(chef):
                try:
                    if chef.email_unsubscribe_hash == None or chef.email_unsubscribe_hash == '':
                        chef.email_unsubscribe_hash = chef.generate_random_email_hash()
                        chef.save()
                    s.subscribe(name=chef.name, email=chef.email, list_id=list.list_id, hash=chef.email_unsubscribe_hash)
                    list.chefs.add(chef)
                except:
                    pass
                
        return True
    
    def unsubscribe_chef(self, chef):
        
        s = Sendy(base_url=settings.SENDY_URL)
        
        lists = chef.emailing_lists.all()
        for list in lists:
            try:
                s.unsubscribe(email=chef.email, list_id=list.list_id)
                chef.email_newsletter = False
                chef.save()
                list.chefs.remove(chef)
            except:
                pass
            
        return True

    
class EmailingList(models.Model):
    
    LIST_TYPE_SENDY = 0
    LIST_TYPE_HUBSPOT = 1
    LIST_TYPES = (
             (LIST_TYPE_SENDY, 'SENDY'),
             (LIST_TYPE_HUBSPOT, 'HUBSPOT'),
             )
    
    CHEF_TYPE_ALL = -1
    CHEF_TYPE_FOODIE = 0
    CHEF_TYPE_CHEF = 1
    CHEF_TYPES = (
             (CHEF_TYPE_ALL, 'ALL'),
             (CHEF_TYPE_FOODIE, 'FOODIE'),
             (CHEF_TYPE_CHEF, 'CHEF'),
             )

    list_type = models.IntegerField(blank=False, choices=LIST_TYPES, default=LIST_TYPE_SENDY)
    list_id = models.CharField(max_length=255, blank=False)
    list_name = models.CharField(max_length=128, blank=False)
    
    language = models.CharField(max_length=3, default="ALL")
    country = models.CharField(max_length=4, blank=False, default="ALL")
    min_recipes = models.IntegerField(default=0, blank=False)
    max_recipes = models.IntegerField(default=1000, blank=False)
    chef_type = models.IntegerField(blank=False, choices=CHEF_TYPES, default=CHEF_TYPE_ALL)
    last_login_after = models.IntegerField(default=0, blank=False)
    last_login_before = models.IntegerField(default=10000, blank=False)
    chefs = models.ManyToManyField(Chefs, related_name="emailing_lists", blank=True)
    page = models.IntegerField(default=0, blank=False)
    page_size = models.IntegerField(default=1000000, blank=False)
    
    objects = EmailingListManager()
    
    class Meta:
        app_label = 'emailing'
        db_table = 'emailing_lists'
        verbose_name_plural = 'Emailing Lists'
    
    
    def check_match(self, chef):
        
        if chef.cache_recipes < self.min_recipes:
            return False
        
        if chef.cache_recipes > self.max_recipes:
            return False
        
        if self.last_login_after != 0 and chef.last_login > datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=self.last_login_after):
            return False
        
        if self.last_login_before != 0 and chef.last_login < datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=self.last_login_before):
            return False
        
        if self.language.lower() != 'all':
            if chef.language.lower() == 'en':
                return self.language != 'es'
            
            if chef.language.lower() != self.language.lower():
                return False
            
        if self.country.lower() != 'all':
            if chef.country.lower() != self.country.lower():
                return False
            
        if self.chef_type != -1:
            if chef.type != self.chef_type:
                return False
        
        return True
        