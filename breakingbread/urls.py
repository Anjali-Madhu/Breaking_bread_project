from django.urls import path
from breakingbread import views

app_name = 'breakingbread'
urlpatterns = [
path('', views.index, name='index'),
path('register/', views.register, name='register'),
path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
path('receipe-post.html', views.recipe, name='recipe'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('cuisine/',views.cuisine_list,name='cuisine'),
path('search-results/',views.search,name='search'),
path('recipes/<str:userid>/',views.search,name="search_name"),
path('browse/category/<str:category>/',views.search,name='browse_category'),
path('browse/level/<str:level>/',views.search,name='browse_level'),
path('browse/cuisine/<str:cuisine>/',views.search,name='browse_cuisine'),
path('my-details/',views.user_details,name="details"),
path('upload_recipe/', views.UploadRecipe.as_view(), name='upload_recipe'),
]
