from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_page, name="register"),

    path('', views.home, name='home'),
    path('group/<str:pk>', views.group, name='group'),

    path('create-group/', views.create_group, name="create-group"),
    path('update-group/<str:pk>', views.update_group, name="update-group"),
    path('delete-group/<str:pk>', views.delete_group, name="delete-group"),

    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
]
