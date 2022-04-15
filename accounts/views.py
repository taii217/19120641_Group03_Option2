from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    return render(request,'accounts\dashboard.html')

def products(request):
    return render(request,'accounts\products.html')

def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)
    if(not customer):
        return render(request,'accounts\customer.html',context)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request,'accounts\customer.html',context)