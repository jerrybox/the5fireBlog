from django.contrib import admin

import xadmin

from comment.models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin:
    list_display = ('target', 'nick_name', 'content', 'website', 'created_time')
