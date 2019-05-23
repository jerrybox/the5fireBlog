from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """admin管理基类：
    1 限制用户只能看到自己创建的内容
    2 创建修改内容后，操作者自动保存为当前用户
    """
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
