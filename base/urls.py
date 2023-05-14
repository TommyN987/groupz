from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('group/<str:pk>', views.group, name='group'),

    path('create-group/', views.create_group, name="create-group"),
    path('update-group/<str:pk>', views.update_group, name="update-group"),
    path('delete-group/<str:pk>', views.delete_group, name="delete-group")
]
