from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.shortcuts import reverse
from django.utils.html import format_html

import xadmin
from xadmin.filters import manager, RelatedFieldListFilter
from xadmin.layout import Row, Fieldset, Container

from blog.adminforms import PostAdminForm
from blog.models import Post, Tag, Category
from typeidea.custom_site import custom_site
from typeidea.base_xadmin import BaseOwnerAdmin


BaseOwnerAdmin = object  # 显示所有的文章


@xadmin.sites.register(LogEntry)
class LogEntryAdmin:
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户创建的分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'  # url上参数的名称

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, reqeust, params, model, admin_view, field_path):
        super().__init__(field, reqeust, params, model, admin_view, field_path)
        self.lookup_choices = Category.objects.filter(owner=reqeust.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)


class PostInline:
    # fields = ('title', 'desc')
    form_layout =(
        Container(
            Row('title', 'desc'),
        )
    )
    extra = 1  # 除了现有关联对象，空白的对象有几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')
    readonly_fields = ('owner',)

    inlines = [PostInline,]

    # 自定义字段
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')
    readonly_fields = ('owner',)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    list_display_links = []

    # exclude = ('owner',)

    list_filter = ['category', ]  # 自定义过滤器
    search_fields = ['title', 'category__name',]

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True
    filter_horizontal = ('tag',)

    form_layout = (
        Fieldset(
            '基础信息',
            Row('tiltle', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )

    # 自定义字段
    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>'.format(
                reverse('xadmin:blog_post_change', args=(obj.id,))
            )
        )
    operator.short_description = '操作'

    form = PostAdminForm  # 自定义字段的html标签

