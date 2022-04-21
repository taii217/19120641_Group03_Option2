from multiprocessing import context
from tokenize import group
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory

from accounts.decorators import unauthenticated_user
from .models import *

from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from .decorators import admin_only, unauthenticated_user,allowed_users

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request,'Accounts was created for ' + username)
            return redirect('login')
    context ={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else :
            messages.info(request,'User or password is incorrect')

    context ={}
    return render(request,'accounts/login.html',context)
    
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    orders_count = orders.count()
    orders_delivered_count = orders.filter(status ="Delivered").count()
    orders_pending_count = orders.filter(status ="Pending").count()
    print('ORDERS:',orders)

    context = { 'orders':orders,
                'orders_count':orders_count,
                'orders_delivered_count':orders_delivered_count,
                'orders_pending_count':orders_pending_count
            }
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)
    if request.method =='POST':
        form = CustomerForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
        
    context ={'form':form}
    return render(request,'accounts/account_settings.html',context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    context ={'products':products}
    return render(request,'accounts\products.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts\customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context ={'item':order}
    return render(request, 'accounts\delete.html',context)
