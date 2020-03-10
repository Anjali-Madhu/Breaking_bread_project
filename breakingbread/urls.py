from django.urls import path
from breakingbread import views

app_name = 'breakingbread'
urlpatterns = [
path('', views.index, name='index'),
path('register/', views.register, name='register'),
path('recipe/', views.recipe, name='recipe'),
path('receipe-post.html', views.recipe, name='recipe'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('cuisine/',views.cuisine_list,name='cuisine')


        ]