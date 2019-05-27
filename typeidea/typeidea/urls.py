"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from .custom_site import custom_site
from blog.views import (
    post_list,
    post_detail,
    links,
    IndexView,
    PostDetailView,
    CategoryView,
    TagView,
    )


urlpatterns = [
    url('^$', IndexView.as_view()),
    url('^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url('^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url('^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url('^links/$', links, name='links'),

    # admin
    url(r'^admin/', admin.site.urls),
    url(r'^custom_admin/', custom_site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
