from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.


@unauthenticated_user
def register_page(request):

    # form = UserCreationForm()             Default django form
    form = CreateUserForm()  # Our own custom form

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            #     name=username,
            #     email=email,
            # )

            # messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('login')
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    cust_orders = request.user.customer.order_set.all()
    total_orders = cust_orders.count()
    delivered = cust_orders.filter(status='Delivered').count()
    pending = cust_orders.filter(status='Pending').count()
    context = {'cust_orders': cust_orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers': customers, 'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, id):
    curr_customer = Customer.objects.get(id=id)
    cust_orders = curr_customer.order_set.all()  # gives all the orders where customer_id foreign key is curr_customer
    orders_count = cust_orders.count()

    myFilter = OrderFilter(request.GET, queryset=cust_orders)
    cust_orders = myFilter.qs

    context = {'curr_customer': curr_customer, 'cust_orders': cust_orders, 'orders_count': orders_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


# Without formset
# def create_order(request, id):
#
#     customer = Customer.objects.get(id=id)
#     form = OrderForm(initial={'customer': customer})        # initial is used to set initial values of some form fields
#                                                             # 'customer' => name in the Order model field
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {'form': form}
#     return render(request, 'accounts/order_form.html', context)


# using form set
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(instance=customer)  # the objects that are in the database are shown by default
    # we want to add new items to the database, so do not specify the initial details
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, id):
    order = Order.objects.get(id=id)
    formset = OrderForm(instance=order)  # by using instance = order, we are filling the whole form by
    # the model data
    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = {'form': form}
    return render(request, 'accounts/user_settings.html', context)
