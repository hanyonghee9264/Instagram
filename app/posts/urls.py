from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # posts.urls내의 패턴들은, perfix가 '/posts/'임
    path('', views.post_list, name='post-list'),
    path('create/', views.post_create, name='post-create'),
]
