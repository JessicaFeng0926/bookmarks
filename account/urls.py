from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # 登录
    # path('login/',views.user_login,name='login'),
    # 用django的登录视图类登录
    #path('login/',auth_views.LoginView.as_view(),name='login'),
    #path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # 网站的主页，这是非常重要的，不能注释
    path('',views.dashboard,name='dashboard'),
    # 修改密码
    #path('password_change/',auth_views.PasswordChangeView.as_view(),
    #name='password_change'),
    #path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),
    #name='password_change_done'),
    # 重置密码
    #path('password_reset/',auth_views.PasswordResetView.as_view(),
    #name='password_reset'),
    #path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),
    #name='password_reset_done'),
    #path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),
    #name='password_reset_confirm'),
    #path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),
    #name='password_reset_complete'),
    # 这一个url设置就相当于前面所有跟登录密码相关的url了
    path('',include('django.contrib.auth.urls')),
    # 注册
    path('register/',views.register,name='register'),
    # 修改个人信息
    path('edit/',views.edit,name='edit'),
]