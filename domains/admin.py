from django.contrib import admin

from .models import Website


class SiteAdminModel(admin.ModelAdmin):
    list_display = ('domain',)

    fieldsets = (
        ('Main', {
            'fields': ['url', ]
        }),

        ('Test', {
            'fields': ['owner']
        })
    )


admin.site.register(Website, SiteAdminModel)