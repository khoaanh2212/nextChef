from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from chefs.models import Chefs, Restaurant
from domain.chefs.plan.Plan import Plan
from chefs.forms import UserChangeForm, ChefsCreationForm
from recipe.models import Recipes


class ChefsAdmin(UserAdmin):
    list_per_page = 20
    form = UserChangeForm
    add_form = ChefsCreationForm
    list_display = ('id', 'email', 'type', 'noted', 'is_staff', 'cache_recipes', 'username', 'name', 'surname',
                    'is_active', 'final_score', 'onboard_score', 'onboard_languages','fb_user_id', 'country')
    list_editable = ('onboard_score', 'onboard_languages')
    list_filter = ('noted', 'is_superuser', 'country')
    fieldsets = (
        (None, {'fields': ('email', 'type', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'location', 'short_bio', 'description',
                                      'onboard_languages')}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
        ('Rank info', {'fields': ('noted', 'manual_score', 'final_score', 'onboard_score')}),
        ('Important dates', {'fields': ('last_signin_date', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide', ), 'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('id', 'email', 'username', 'id')
    ordering = ('-creation_date',)
    filter_horizontal = ()


class RestaurantAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'web', 'address', 'zip', 'city', 'country', )
    list_filter = ('name',)
    search_fields = ('name',)
    filter_horizontal = ()

    raw_id_fields = ('chef',)
    related_lookup_fields = {
        'fk': ['chef']
    }

admin.site.register(Chefs, ChefsAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Plan)
