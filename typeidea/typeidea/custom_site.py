from django.contrib import admin


class CustomSite(admin.AdminSite):
    site_header = 'TypeIdea'
    site_title = 'TypeIdea 管理后台'
    index_title = '首页'

custom_site = CustomSite(name='custom_site')  # 相当于namespace
