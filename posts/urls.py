from django.urls import path

from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница группы
    path('group/<slug:slug>', views.group, name='group'),
    # Страница со списком всех групп
    path('groups/', views.groups, name="groups"),
    # Страница создания нового поста
    path('new/', views.new_post, name="new_post"),
    # Страница создания новой группы
    path('create_group/', views.create_group, name="create_group"),
    # Редактирование группы
    path('group/<slug:slug>/edit/', views.group_edit, name='group_edit'),
    # Страница удаления группы
    path('delete_group/<slug:slug>', views.delete_group, name="delete_group"),
    # Лента с поставми любимых авторов
    path("follow/", views.follow_index, name="follow_index"),
    # Подписка на автора
    path("<username>/follow/", views.profile_follow, name="profile_follow"),
    # Отписка от автора
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    # Профайл пользователя
    path("<username>/", views.profile, name="profile"),
    # Просмотр записи
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    # Редактирование записи
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    # Удаление записи
    path("<username>/<int:post_id>/delete/",
         views.post_delete, name="post_delete"),
    # Добавление комментариев
    path("<username>/<int:post_id>/comment",
         views.add_comment, name="add_comment"),
]
