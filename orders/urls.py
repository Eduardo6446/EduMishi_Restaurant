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
    path('check/', views.check, name='check'),
    path('updaterecords/<int:order_id>', views.updaterecords, name='updaterecords'), # redirects to the update
    path('item/delete/<item_id>)/', views.delete_from_cart, name='delete_item'),
    path('success/', views.success, name='success'),
    path('ordersummary/', views.order_details, name="ordersummary"),
    path('customize_order/str<food>', views.customize_order, name="customize_order"),
    path('add-to-cart/<int:item_id>', views.add_to_cart, name="add_to_cart"),

]

#<td> <a> <button type="submit" href="{% url 'orders:updaterecords' order.id %}" class="pull-right btn btn-primary">Checkout</button></a></td>