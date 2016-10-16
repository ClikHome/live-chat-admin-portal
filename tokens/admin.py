from django.contrib import admin
from django.db import models
from .models import Token, TokenDuration


class TokenDurationAdmin(admin.ModelAdmin):
    list_display = ('title', 'days', 'months', 'years', 'is_active')

    fieldsets = (
        (None, {
            'fields': ('title', 'is_active')
        }),

        ('Time', {
            'fields': ('days', 'months', 'years')
        })
    )


class TokenAdmin(admin.ModelAdmin):
    list_display = ('uid', 'duration', 'remaining_time', 'expiry_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('uid',)
    readonly_fields = ("created_at", 'remaining_time' ,) # 'is_used', 'is_active')
    fieldsets = (
        ('Token', {
            'fields': ('uid', 'channel', 'duration')
        }),

        ('Flags', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('is_active', 'is_used',)
        }),

        ('Activation', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('started_at', 'expiry_at')
        }),

        ('Timedelta', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('remaining_time' , 'duration')
        }),

    )


admin.site.register(Token, TokenAdmin)
admin.site.register(TokenDuration, TokenDurationAdmin)