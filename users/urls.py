from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name = 'users'),
    path('users/register/', views.users_create, name = 'users_register'),
    path('users/<int:id>/', views.users_detail, name = 'users_detail'),
    path('login/', views.loginn, name = 'login'),
    path('logout/', views.logoutt, name = 'logout')
]