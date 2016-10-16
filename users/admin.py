from django.contrib import admin

from .models import ChatUser, ChatUserRole, UserBan
from messages.models import Message


class ChatUserBannes(admin.TabularInline):
    model = UserBan
    verbose_name = 'ban'
    verbose_name_plural = 'Bannes'
    extra = 0
    max_num = 10

    fields = ('reason', 'created_at', 'expiry_at', 'is_permanent')
    readonly_fields = fields
    classes = ('grp-collapse grp-closed',)


class ChatUserMessagesInline(admin.TabularInline):
    model = Message
    verbose_name = 'message'
    verbose_name_plural = 'Messages'
    extra = 0
    max_num = 20
    can_delete = True

    fields = ('body', 'created_at', 'is_active')
    readonly_fields = fields
    classes = ('grp-collapse grp-closed',)



class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_channel_title', 'is_active')
    fields = ('username', 'channel')
    list_filter = ('is_active', 'channel')
    search_fields = ('username', 'channel')

    inlines = [ChatUserMessagesInline, ChatUserBannes]

    def get_channel_title(self, obj):
        return obj.channel.title

    get_channel_title.short_description = 'Channel Title'
    get_channel_title.admin_order_field = 'channel__title'


admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(UserBan)