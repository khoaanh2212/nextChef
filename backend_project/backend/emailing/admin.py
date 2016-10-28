import datetime

from django.contrib import admin

from .models import EmailingList
from chefs.models import Chefs
from pysendy import Sendy

class EmailingListAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('list_name', 'list_type', 'list_id', 'language', 'country', 'min_recipes', 'max_recipes', 'chef_type', 'last_login_after', 'last_login_before', 'page', 'page_size')
    list_filter = ('list_name',)
    search_fields = ('list_name',)
    filter_horizontal = ()
    
    raw_id_fields = ('chefs',)
    related_lookup_fields = {
        'm2m': ['chefs']
    }
    
    actions = ['update_list']

    def update_list(self, request, queryset):
        for list in queryset:
            
            chefs = Chefs.objects.filter(email_newsletter=True) 
            chefs = chefs.filter(cache_recipes__gte=int(list.min_recipes))
            chefs = chefs.filter(cache_recipes__lte=int(list.max_recipes))
            
            #if list.language.lower() != 'all':
            #    chefs = chefs.filter(language=list.language.lower())
            
            if list.language.lower() != 'all':
                
                if list.language.lower() == 'en':
                    chefs = chefs.all().exclude(language='es')
                else:
                    chefs = chefs.filter(language=list.language.lower())
                
            if list.country.upper() != 'ALL':
                chefs = chefs.filter(country=list.country.upper())
            
            if list.chef_type != -1:
                chefs = chefs.filter(type=list.chef_type)
            
            if list.last_login_before != None and list.last_login_before != '':
                before_date = datetime.datetime.now() - datetime.timedelta(days=list.last_login_before)
                chefs = chefs.filter(last_login__gte=before_date)
             
            if list.last_login_after != None and list.last_login_after != '':
                after_date = datetime.datetime.now() - datetime.timedelta(days=list.last_login_after)
                chefs = chefs.filter(last_login__lte=after_date)
            
            chefs_init = list.page * list.page_size 
            chefs_end = list.page * list.page_size + list.page_size
            
            chefs = chefs[chefs_init:chefs_end]
            s = Sendy(base_url='http://mailing.nextchef.co')
            
            old_chefs = list.chefs.all()
            for old_chef in old_chefs:
                if not old_chef in chefs:
                    try:
                        s.unsubscribe(email=old_chef.email, list_id=list.list_id)
                        list.chefs.remove(old_chef)
                    except:
                        pass
                    
            for chef in chefs:
                if not chef in old_chefs:
                    try:
                        if chef.email_unsubscribe_hash == None or chef.email_unsubscribe_hash == '':
                            chef.email_unsubscribe_hash = chef.generate_random_email_hash()
                            chef.save()
                        s.subscribe(name=chef.name, email=chef.email, list_id=list.list_id, hash=chef.email_unsubscribe_hash, language=chef.language)
                        list.chefs.add(chef)
                    except:
                        pass
        
    update_list.short_description = "Update List"
    
admin.site.register(EmailingList, EmailingListAdmin)
