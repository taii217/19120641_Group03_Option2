from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import ModelForm, OrderForm
from .filters import OrderFilter
# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orders_count = orders.count()
    customers_count = customers.count()
    orders_delivered_count = orders.filter(status ="Delivered").count()
    orders_pending_count = orders.filter(status ="Pending").count()

    context ={'customers':customers,
                'orders':orders,
                'orders_count':orders_count,
                'customers_count':customers_count,
                'orders_delivered_count':orders_delivered_count,
                'orders_pending_count':orders_pending_count
            }
    
    
    return render(request,'accounts\dashboard.html',context)

def products(request):
    products = Product.objects.all()
    context ={'products':products}
    return render(request,'accounts\products.html',context)

def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts\customer.html',context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing form', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={'formset':formset}
    return render(request,'accounts\order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={'form':form}
    return render(request,'accounts\order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context ={'item':order}
    return render(request, 'accounts\delete.html',context)
