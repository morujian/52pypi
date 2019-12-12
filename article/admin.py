from django.contrib import admin
# 导入需要注册到管理后台的数据模型类
from .models import ArticlePost

# Register your models here.
# 注册数据模型类到admin的管理后台中
admin.site.register(ArticlePost)
