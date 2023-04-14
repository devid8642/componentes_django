from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name = 'users'),
    path('users/create/', views.users_create, name = 'users_create'),
    path('users/<int:id>/', views.users_detail, name = 'users_detail')
]