from django.db import models
# 导入django内建的User模型
from django.contrib.auth.models import User
# 导入timezone处理时间相关的事物
from django.utils import timezone
# 引入markdown编辑器的模块方法
from mdeditor.fields import MDTextField
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# 记得导入
from django.urls import reverse


# Create your models here.
# 定义一个文章的模型类
class ArticlePost(models.Model):
    # 文章作者字段，关联到Django内建的User表
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    # 文章的标题字段,models.CharField用来保存较短的字符串
    title = models.CharField(max_length=100, verbose_name='标题')
    # 文章标题图
    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d/',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        verbose_name='标题图',
    )
    # 文章的正文，models.TextField保存大量文本，改用MDTextFied
    body = MDTextField(verbose_name='正文', config_name='form_config')
    # 文章的创建时间，default=timezone.now表示在创建数据时，自动写入当前时间
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    # 文章的更新时间，auto_now=True表示更新数据时，自动写入当前时间
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 阅读量
    total_views = models.PositiveIntegerField(default=0)

    # 内部类 Meta用于定义模型的元数据
    class Meta:
        # ordering表示数据的排序
        # '-created'表示按照时间进行倒序排列，最近的在最前面
        ordering = ('-created',)

    # __str__方法定义了，当调用对象的str()方法时，返回值的内容
    def __str__(self):
        return self.title
