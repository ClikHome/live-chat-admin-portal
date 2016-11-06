from django.contrib import admin

from .models import Channel
from domains.models import Website
from tokens.models import Token


class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 0

    # def formfield_for_manytomany(self, db_field, request=None, **kwargs):
    #     print db_field.name
    #     return super(ChannelInline, self).formfieor_foreignkey(db_field, request, **kwargs)
    #
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     object_id = int(request.resolver_match.args[0])

    def __init__(self, *args, **kwargs):
        super(ChannelInline, self).__init__(*args, **kwargs)

        building_id = self.fields
        # building = Channel.objects.get(id=building_id)

        self.obj = args[0] if args else None
        self.obj2 = args[1]

    def get_queryset(self, request):
        object_id = int(request.resolver_match.args[0])
        filtered_objects = list(Website.objects.all())[object_id - 1]

        try:
            owner = Channel.objects.get(pk=object_id)
        except Channel.DoesNotExist:
            owner = None

        return self.model.objects.filter(channel__owner=request.user)


class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_active', 'created_at', 'owner', 'status')
    inlines = [ChannelInline]

    fieldsets = (
        ('Title', {
            'fields': ('url',)
        }),

        ('Settings', {
            'fields': ('owner', 'is_active')
        })
    )


class TokenInline(admin.TabularInline):
    model = Token
    fk_name = 'channel'
    extra = 0
    classes = ('grp-collapse grp-open',)


class DomainsInline(admin.TabularInline):
    model = Channel
    extra = 0

    def get_queryset(self, request):
        return self.model.objects.all()


class Domains2Inline(admin.TabularInline):
    model = Website
    extra = 0


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_active')
    list_filter = ('is_active', 'owner')
    search_fields = ('title',)
    readonly_fields = ('uid',) # !!! add 'owner',
    # exclude = ('sites', )

    fieldsets = (
        ('Title', {
            'fields': ('title', 'uid')
        }),

        ('Users', {
            'fields': ('owner',)
        }),
    )

    def __init__(self, *args, **kwargs):
        super(ChannelAdmin, self).__init__(*args, **kwargs)


admin.site.register(Channel, ChannelAdmin)