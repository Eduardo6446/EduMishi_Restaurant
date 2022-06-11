from django.urls import path
from django.shortcuts import render

from . import views

app_name = 'orders'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path('profile', views.profile, name='profile'),
    path('allorders', views.allorders, name='allorders'),


]
