from django.contrib import admin
from .models import Team
from django.utils.html import format_html

class TeamAdmin(admin.ModelAdmin):
    # this function to create a thumbnail
    # the parameter object  represent the Team object
    def thumbnail(self, object):
        return format_html('<img src="{}" width=40px style="border-radius:50px;"/>'.format(object.photo.url))
    # the description which will be shown in Team table
    thumbnail.short_description = "Photos"
    # the field will be shown in Team table
    list_display = ("id", "thumbnail", "first_name", "designation", "created_date",)
    # clickable field which takes us to row detail
    list_display_links = ("id", "first_name",)
    # the field which we can make a search based on
    search_fields = ('first_name', 'last_name', 'designation')
    # filter based on a field
    list_filter = ('designation',)


# Register your models here.
admin.site.register(Team, TeamAdmin)
