from django.contrib import admin

from config.models import Link, SideBar


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'href', 'weight', 'owner', 'created_time')
    fields = ('title', 'status', 'href', 'weight',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'status', 'content', 'owner', 'created_time')
    fields = ('title', 'display_type', 'content',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
