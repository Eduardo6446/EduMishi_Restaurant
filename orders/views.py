from textwrap import dedent
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

from .models import (Topping, Menu_Item, Profile,
Extras, Order, OrderItem,  User, )

import datetime



# Create your views here.
@login_required()
def index(request):

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    menu_items = Menu_Item.objects.exclude(category__icontains="Topping") \
    .exclude(category__icontains="Extra")

    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []

    item_count = 0

    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.ordered_items.all()
        current_order_products = [menu_item.menu_item for menu_item
                                in user_order_items]

        #toma el numero de items en el carrito
        item_count = user_order.ordered_items.count()

    context ={

        'current_order_products': current_order_products,
        'item_count': item_count,
        "user": request.user,
        "menu_item": menu_items.order_by('-category')
    }
    return render(request, "orders/index.html", context)

def login_view(request):

    if request.method == "GET":

        return render(request, "orders/login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("orders:index"))
    else:
        return render(request, "orders/login.html", {"message": "Datos invalidos."})

def logout_view(request):

    logout(request)

    return render(request, "orders/login.html",
        {"message": "Saliste de la cuenta."})

def register_view(request):

    if request.method == 'GET':
        return render(request, 'orders/register.html')

    user = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['confirm_password']

    """ validate credentials server side"""
    if not user:
        return render(request, 'orders/register.html',
                        {"message": "ponga el usuario ombe."})

    if len(user) < 4:
        return render(request, 'orders/register.html',
         {"message": "mayor a 4 caracteres."})

    if not email:
        return render(request, 'orders/register.html',
        {"message": "xd"})

    # Email validation required.
    if not password or not password_confirmation:
        return render(request, 'orders/register.html',
        {"message": "ingrese algo valido"})

    if password != password_confirmation:
        return render(request, 'orders/register.html',
        {"message": "no coincide"})

    if len(password) < 4 or len(password_confirmation) < 4 :
        return render(request, 'orders/register.html',
        {"message": "La contraseña debe ser mayor a 4 ."})

    try:
        User.objects.create_user(user, email, password)
    except:
        return render(request, 'orders/register.html',
        {"message": "Algo a fallado al registrarte."})

    if first_name:
        User.first_name = first_name
    if last_name:
        User.last_name = last_name
    return HttpResponseRedirect(reverse('orders:login'))


@login_required()
def profile(request):

    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)


    context = { 'my_orders': my_orders, 'user': request.user}

    return render(request, "orders/profile.html", context)

def allorders(request):

    profiles = Profile.objects.all()
    all_orders = Order.objects.filter(is_ordered=True)

    context = { 'all_orders': all_orders}

    return render(request, "orders/allorders.html", context)

@login_required()
def get_user_pending_order(request):
    # obtener el pedido para el usuario correcto
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # obtener el único pedido en la lista de pedidos filtrados con is_ordered = False
        return order[0]
    return 0

@login_required()
def check(request, **kwargs):
    existing_order = get_user_pending_order(request)

    context = {
        'order': existing_order,
    }

    return render(request, 'orders/check.html', context)