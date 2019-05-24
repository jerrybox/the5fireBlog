from django.http import HttpResponse
from django.shortcuts import render

from config.models import SideBar
from .models import Tag, Post, Category


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        posts, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts, category = Post.get_by_category(category_id)
    else:
        posts = Post.normal_posts()

    context = {
        'tag': tag,
        'category': category,
        'posts': posts,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


def links(request):
    pass
