from django.contrib import admin


from .models import (Menu_Item,  Extras, Order, OrderItem, Profile, )

admin.site.register(Menu_Item)
admin.site.register(Extras)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
