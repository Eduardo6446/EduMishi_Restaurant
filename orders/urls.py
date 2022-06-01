from django.urls import path
from django.shortcuts import render

from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("home/login", views.login, name="login"),
    path("home/register", views.register, name="register"),
    path("home/cart", views.cart, name="cart")

]
