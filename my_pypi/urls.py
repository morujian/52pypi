"""my_pypi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# 不太懂这引入的模块
from django.conf import settings
from django.conf.urls.static import static
from article.views import article_list
from my_pypi.feeds import LatestEntriesFeed
from my_pypi.views import about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', article_list, name='home'),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('password-reset/', include('password_reset.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('latestfeed/', LatestEntriesFeed(), name='latestfeed'),
    path('about/', about, name='about')
]
# 不太懂这段代码，为上传的图片配置好url路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


