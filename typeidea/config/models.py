from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_CHOICES = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]
    title = models.CharField(max_length=10, verbose_name='标题')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=STATUS_NORMAL, verbose_name='状态')
    href = models.URLField(verbose_name='链接')
    weight = models.PositiveIntegerField(default=1,
                                         choices=zip(range(1,6), range(1,6)),
                                         verbose_name='权重',
                                         help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.title


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '显示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, "HTML"),
        (DISPLAY_LATEST, "最新文章"),
        (DISPLAY_HOT, "最热文章"),
        (DISPLAY_COMMENT, "最近评论"),
    )

    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(choices=SIDE_TYPE, default=DISPLAY_HTML, verbose_name='展示类型')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_SHOW, verbose_name='状态')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容', help_text='如果设置的不是HTML类型可以为空')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        from blog.models import Post
        from comment.models import Comment

        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            posts = Post.latest_posts(num=2).only("title", "id")
            context = {
                'posts':posts,
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context=context)
        elif self.display_type == self.DISPLAY_HOT:
            posts = Post.hot_posts().only("title", "id")
            context = {
                'posts': posts,
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context=context)
        elif self.display_type == self.DISPLAY_COMMENT:
            comments = Comment.objects.filter(status=Comment.STATUS_NORMAL)
            context = {
                'comments':comments,
            }
            result = render_to_string('config/blocks/sidebar_comment.html', context=context)
        return result
