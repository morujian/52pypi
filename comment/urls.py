from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('comment-post/<int:id>/', views.comment_post, name='comment_post')
]
