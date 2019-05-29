

class BaseOwnerAdmin:
    """admin管理基类：
    1 限制用户只能看到自己创建的内容
    2 创建修改内容后，操作者自动保存为当前用户
    """
    exclude = ('owner',)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)
