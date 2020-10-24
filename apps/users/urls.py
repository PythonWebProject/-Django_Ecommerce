from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否存在
    re_path('usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', views.UsernameExists.as_view()),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.MobileExists.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
]