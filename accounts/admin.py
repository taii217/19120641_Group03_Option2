from django.contrib import admin

# Register your models here.
from .models import Customer, Order, Products

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
