from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.shortcuts import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from blog.models import Post, Tag, Category
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')


class CategoryOwnerFilter(admin.SimpleListFilter):
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


class PostInline(admin.TabularInline):
    # fields = ('title', 'desc')
    extra = 1  # 除了现有关联对象，空白的对象有几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')
    readonly_fields = ('owner',)

    list_filter = [CategoryOwnerFilter,]

    inlines = [PostInline,]

    # 自定义字段
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')
    readonly_fields = ('owner',)


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    list_display_links = []

    # exclude = ('owner',)

    list_filter = [CategoryOwnerFilter]  # 自定义过滤器
    search_fields = ['title', 'category__name',]

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (('category','title'),'status',)
        }),
        ('内容', {
            'fields': ('desc', 'content')
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag', ),
        }),
    )

    # 自定义字段
    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>'.format(
                reverse('custom_site:blog_post_change', args=(obj.id,))
            )
        )
    operator.short_description = '操作'

    form = PostAdminForm  # 自定义字段的html标签

    class Media:
        css = {
            'all': ('bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.js.fake',)
