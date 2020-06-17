from django.urls import path

from .import views

app_name = 'images'

urlpatterns = [
    # 这是给一张新图片写标题和描述的路由
    path('create/',views.image_create,name='create'),
    # 展示一张图片
    path('detail/<int:id>/<slug:slug>',views.image_detail,name='detail'),
    # ajax请求点赞的路由
    path('like/',views.image_like,name='like'),
    # 显示所有的图片
    path('',views.image_list,name='list'),
    # 最受欢迎的十张图片
    path('ranking/',views.image_ranking,name='ranking'),
]