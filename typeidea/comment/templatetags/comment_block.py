"""
这个文件必须放在templatetags文件夹下
参考文档：https://docs.djangoproject.com/en/2.2/topics/templates/
"""
from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm,
        'comment_list': Comment.get_by_target(target),
    }
