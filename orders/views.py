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

        return render(request,"orders/login.html")

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

    #validacoin de registro
    if not user:
        return render(request, 'orders/register.html',
                        {"message": "ponga el usuario ombe."})

    if len(user) < 4:
        return render(request, 'orders/register.html',
         {"message": "mayor a 4 caracteres."})

    if not email:
        return render(request, 'orders/register.html',
        {"message": "xd"})

    # validacion de Email.
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
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile) #ojo aqui tambien


    context = { 'my_orders': my_orders, 'user': request.user}

    return render(request, "orders/profile.html", context)


def allorders(request):

    profiles = Profile.objects.all()
    all_orders = Order.objects.filter(is_ordered=False)#ojoooooooooooooooooo aqui si no esta ordenado no sale

    context = { 'all_orders': all_orders}

    return render(request, "orders/allorders.html", context)


@login_required()
def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required()
def check(request, **kwargs):
    existing_order = get_user_pending_order(request)

    context = {
        'order': existing_order,
    }

    return render(request, 'orders/check.html', context)

@login_required()
def updaterecords(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()

    order_items = order_to_purchase.ordered_items.all()

    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    user_profile = get_object_or_404(Profile, user=request.user)

    order_products = [item.menu_item for item in order_items]


    user_profile.menu_items.add(*order_products)
    user_profile.save()

    return redirect(reverse('orders:success'))


@login_required()
def success(request, **kwargs):

    user_profile = get_object_or_404(Profile, user=request.user)
    finished_order = Order.objects.filter(owner=user_profile, is_ordered=True).last()

    context = {
        'order': finished_order,
    }
    return render(request, 'orders/purchase_success.html', context)


@login_required()
def order_details(request, **kwargs):

    existing_order = get_user_pending_order(request)
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)

    context = {
        'order': existing_order,
    }
    return render(request, 'orders/ordersummary.html', context)

@login_required()
def delete_from_cart(request, item_id):

    item_to_delete = OrderItem.objects.filter(pk=item_id)
    deleted_item = OrderItem.objects.get(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, f" {deleted_item.menu_item.sizes} \
            {deleted_item.menu_item.name}  Eliminado del carrito")

    return redirect(reverse('orders:ordersummary'))

@login_required()
def customize_order(request, food, *args,**kwargs):

    if request.method == "GET":


        toppings = Menu_Item.objects.filter(category__contains="Topping")

        extras = Extras.objects.all()

        extra_cheese=Extras.objects.filter(name__icontains="cheese")

        menu_items = Menu_Item.objects.all()

        ordered_item = Menu_Item.objects.filter(name=food).first()

        context ={

                "ordered_item": ordered_item,
                "user": request.user,
                "menu_item": menu_items,
                "toppings": toppings,
                "extras": extras,
                'extra_cheese': extra_cheese

            }
        return render(request, "orders/customize_order.html", context)

    user_profile = get_object_or_404(Profile, user=request.user)

    menu_item = Menu_Item.objects.filter(name=food).first()
    print (f"this is menu item in get {menu_item}")

    toppings = []

    if "Special" in food:
        special_toppings = request.POST.getlist('special_toppings')
        print(f"special_toppings:{special_toppings} \n")
        toppings = special_toppings

        if len(toppings) < 4:

            messages.info(request, "You chose less than 3 toppings! \
             A special pizza needs \
            4 or more toppings! ")

            menu_items = Menu_Item.objects.all()
            toppings = Menu_Item.objects.filter(category__contains="Topping")
            menu_items = Menu_Item.objects.all()
            ordered_item = Menu_Item.objects.filter(name=food).first()

            context ={

                    "ordered_item": ordered_item,
                    "user": request.user,
                    "menu_item": menu_items,
                    "toppings": toppings,

                }
            return render(request, "orders/customize_order.html", context)



    if "Special" not in food and "Pizza" in food:
        topping1 = request.POST["topping1"]
        toppings.append(topping1)

        try:
            topping2 = request.POST["topping2"]
            toppings.append(topping2)
        except MultiValueDictKeyError:
            toppings2 = False

        try:
            topping3 = request.POST["topping3"]
            toppings.append(topping3)

        except MultiValueDictKeyError:
            topping3 = False

    # get the extras
    extras = []

    num_extras = 0

    if menu_item.category == "Subs":
        sub_extras = request.POST.getlist('sub_extras')

        for extra in sub_extras:
            extras.append(extra + "+ .50c")
            num_extras += 1


    sub_extra = Menu_Item.objects.get(name="Sub_Extra")

    extra_price = sub_extra.price
    extras_cost = num_extras * extra_price

    quantity = int(request.POST['quantity'])

    for x in range(quantity):
        order_item = OrderItem.objects.create(menu_item=menu_item,
        ptoppings=toppings, extras=extras, num_extras=num_extras,
        extras_cost=extras_cost )


        user_order, status = Order.objects.get_or_create(owner=user_profile,
                                                        is_ordered=False)

        user_order.ordered_items.add(order_item)

    if status:
        user_order.save()

    messages.info(request, f" {quantity} {menu_item.sizes} {menu_item.name} \
                            añadido al carrito")

    return HttpResponseRedirect(reverse('orders:index'))

@login_required()
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)

    menu_item = Menu_Item.objects.filter(id=kwargs.get('item_id', "")).first() #item id sent from the url

    quantity = int(request.POST['quantity'])


    for x in range(quantity):
        order_item = OrderItem.objects.create(menu_item=menu_item)

        user_order, status = Order.objects.get_or_create(owner=user_profile,
                                                        is_ordered=False)

        user_order.ordered_items.add(order_item)

    if status:
        user_order.save()

    messages.info(request, f" {quantity} {menu_item.sizes} \
                            {menu_item.name} añadido")

    return HttpResponseRedirect(reverse('orders:index'))
