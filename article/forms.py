from django.forms import ModelForm
from .models import ArticlePost


class ArticlePostForm(ModelForm):  # 定义文章模型的表单类
    class Meta:
        model = ArticlePost  # 指明模型的来源
        fields = ('title', 'avatar', 'column', 'body')  # 指明表单包含的字段
