from django.contrib import admin

from .models import Channel
from tokens.models import Token


class TokenInline(admin.TabularInline):
    model = Token
    fk_name = 'channel'
    extra = 3
    classes = ('grp-collapse grp-open',)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'superuser', 'is_active')
    list_filter = ('is_active', 'superuser')
    search_fields = ('title', 'site')
    readonly_fields = ('uid', 'domain') # !!! add 'superuser',

    fieldsets = (
        ('Title', {
            'fields': ('title', 'uid', 'site', 'domain')
        }),

        ('Users', {
            'fields': ('superuser',)
        }),
    )

    inlines = [TokenInline]

admin.site.register(Channel, ChannelAdmin)
