from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Здесь написано, какой URL какую view запускает.
# name нужен, чтобы потом писать {% url 'post_list' %} в шаблонах.
urlpatterns = [
    # /blog/ - список постов.
    path('', views.PostListView.as_view(), name='post_list'),
    # /blog/register/ - регистрация.
    path('register/', views.RegisterView.as_view(), name='register'),
    # /blog/login/ - вход. Используем готовую view от Django.
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='blog/login.html'),
        name='login',
    ),
    # /blog/logout/ - выход. После выхода возвращаем на список постов.
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='post_list'),
        name='logout',
    ),
    # /blog/post/ - еще один URL для списка постов.
    path('post/', views.PostListView.as_view(), name='post_list_alias'),
    # /blog/post/create/ - создание поста.
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    # pk - это id поста в базе, например /blog/post/1/.
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # Удаление конкретного поста по его id.
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # Создание категории.
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
]
