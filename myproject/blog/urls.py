from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='blog/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='post_list'),
        name='logout',
    ),
    path('post/', views.post_list, name='post_list_alias'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('category/create/', views.category_create, name='category_create'),
]
