from django.contrib import admin

from .models import Recipes, Photos, PhotoStyles, RecipesHasTags, Tags


class TagsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class TagsInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': ('tag', )}),
    ]
    model = RecipesHasTags
    raw_id_fields = ('tag',)
    autocomplete_lookup_fields = {
        'fk': ['tag'],
    }
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'full_url', 'chef', 'nb_likes', 'noted','explore_noted', 'private', 'draft', 'manual_score', 'final_score', 'creation_date',)
    list_filter = ('noted', 'private', 'draft', 'language')
    list_editable = ('noted','explore_noted', 'manual_score')
    search_fields = ('id', 'name','chef__email', 'chef__name')
    fieldsets = (
        ("General", {'fields': ('chef', 'name', 'description', 'language', 'creation_date')}),
        ("Visibility", {"fields": ("private", "draft", "to_sell")}),
        ('Rank info', {'fields': ('noted','explore_noted', 'manual_score', 'final_score')}),
        ('Photos', {'fields': ('admin_cover',)})
    )
    ordering = ('-creation_date',)
    filter_horizontal = ()
    readonly_fields = ('creation_date', 'admin_cover')
    inlines = (TagsInline, )

    raw_id_fields = ('chef',)
    related_lookup_fields = {
        'fk': ['chef']
    }

    def admin_cover(self, obj):
        """
        This method is used in django admin to show the recipe cover in edit form.
        """
        if obj.cover_image:
            return u'<img src="%s" height="300" width="400" />' % obj.cover_image.url
        else:
            return 'Without cover'
    admin_cover.short_description = "Cover"
    admin_cover.allow_tags = True


class PhotoStylesInline(admin.TabularInline):
    model = PhotoStyles


class PhotosAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'is_cover', 'list_s3_url', 'list_image_url', 'creation_date',)
    search_fields = ('id', 'recipe__pk')
    fields = ('chef', 'recipe', 'name', 'is_cover', 'instructions', 'time', 'temperature', 'quantity', 's3_url', 'image_url')
    readonly_fields = ('chef', 'recipe', 'creation_date', )
    inlines = [PhotoStylesInline, ]

    def list_s3_url(self, obj):
        if obj.s3_url:
            if obj.s3_url.name.startswith('http'):
                return u'<a href="%s">%s</a>' % (obj.s3_url.name, obj.s3_url.name)
            else:
                return u'<a href="%s">%s</a>' % (obj.s3_url.url, obj.s3_url.name)
        else:
            return u'No photo'
    list_s3_url.short_description = "s3_url"
    list_s3_url.allow_tags = True

    def list_image_url(self, obj):
        if obj.image_url and obj.image_url.name and obj.image_url.url:
            return u'<a href="%s">%s</a>' % (obj.image_url.url, obj.image_url.name)
        else:
            return u'No photo'
    list_image_url.short_description = "image_url"
    list_image_url.allow_tags = True

admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Tags, TagsAdmin)
