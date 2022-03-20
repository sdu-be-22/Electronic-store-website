from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json


def store(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(name__contains=q)
    else:
        products = Product.objects.all()

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")
    else:
        products = products.order_by("orderitem__date_added")

    context = {'products': products}
    return render(request, 'store/store.html', context)


def basket(request):
    # request.user.customer = request.user.username
    # print(request.user.customer)
    # if request.user.customer.RelatedObjectDoesNotExist:
    #     print('iofewj')
    #     return
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_basket_total': 0, 'get_basket_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/Basket.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_basket_total': 0, 'get_basket_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def smartphones(request):
    products = Product.objects.all()

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/smartphones.html', context)


def laptops(request):
    products = Product.objects.all()

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/laptops.html', context)


def cameras(request):
    products = Product.objects.all()

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/cameras.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def home(request):
    return render(request, 'home.html')


def register(request):
    form = UserCreationForm
    if request.method == 'POST':
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            user = regForm.save()
            messages.success(request, 'User has been registered.')
            Customer.objects.create(user=user, name=user.username, email='test@tx.com')
    return render(request, 'registration/register.html', {'form': form})



