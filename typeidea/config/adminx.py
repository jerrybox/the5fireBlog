from django.contrib import admin

import xadmin

from config.models import Link, SideBar


@xadmin.sites.register(Link)
class LinkAdmin:
    list_display = ('title', 'status', 'href', 'weight', 'owner', 'created_time')
    fields = ('title', 'status', 'href', 'weight',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(SideBar)
class SideBarAdmin:
    list_display = ('title', 'display_type', 'status', 'content', 'owner', 'created_time')
    fields = ('title', 'display_type', 'content',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
