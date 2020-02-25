from django.urls import path
from breakingbread import views

app_name = 'breakingbread'
urlpatterns = [
path('', views.index, name='index'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),


        ]