from django.contrib import admin
from .models import Product, Cart, Entry, Order, OrderItem


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Entry)
admin.site.register(Order)
admin.site.register(OrderItem)