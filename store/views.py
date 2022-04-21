from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.views.generic import ListView
import json
from .forms import CommentForm, EmailForm
from django.shortcuts import render


def index(request): # here all are work fine #
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

    brands = Product.objects.all().order_by('brandName').values('brandName').distinct()
    recentlyViewedProducts = Product.objects.all().order_by('-last_visit')

    context = {'products': products, 'brands': brands, 'recentlyViewedProducts': recentlyViewedProducts}

    return render(request, 'store/index.html', context)


def cart(request): # here all are not work fine#
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_basket_total': 0, 'get_basket_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

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


def checkout(request): #start#
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_basket_total': 0, 'get_basket_items': 0}

    # context = {'items': items, 'order': order}

    # create a variable to keep track of the form
    messageSent = False

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an email with Django from BuyDream shop"
            # message = cd['message']
            message = "Уважаемый " + str(cd['name']) + " Мы приняли ваш заказ, ожидайте свой заказ, по следующему указанному адресу: " + str(cd['city']) + ", " + str(cd['address']) + ". Курьер  заранее вам позванит."
            message = message + ". Стоимость вашего заказа: $" + str(order.get_basket_total) + ". Можете оплатить удобным вам образом."
            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [cd['recipient']])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'store/checkout.html', {

        'form': form,
        'messageSent': messageSent,
        'items': items,
        'order': order,

    }) #end#


def shop(request):
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

    brands = Product.objects.all().order_by('brandName').values('brandName').distinct()

    context = {'products': products, 'brands': brands}

    return render(request, 'store/shop.html', context)


def productView(request, myid):
    product = Product.objects.get(id=myid)
    comments = product.comments.filter(active=True)
    new_comment = None
    product.last_visit = datetime.now()
    product.save()


    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    context = {'product': product,
               'parameters': product.parameter_names.all(),
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form}
    return render(request, "store/singleProduct.html", context)


def smartphones(request):
    products = Product.objects.filter(prTypes='Smartphones')

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/smartphones.html', context)


def laptops(request):
    products = Product.objects.filter(prTypes='Laptops')

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/laptops.html', context)


def cameras(request):
    products = Product.objects.filter(prTypes='Cameras')

    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")

    context = {'products': products}
    return render(request, 'store/cameras.html', context)


def register(request):
    form = UserCreationForm
    if request.method == 'POST':
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            user = regForm.save()
            messages.success(request, 'User has been registered.')
            Customer.objects.create(user=user, name=user.username, email='test@tx.com')
    return render(request, 'registration/register.html', {'form': form})


def brandView(request, brandName):
    products = Product.objects.all().filter(brandName=brandName)
    context = {'products': products}
    return render(request, "store/brandView.html", context)













# previous version

# def store(request):
#     if 'q' in request.GET:
#         q = request.GET['q']
#         products = Product.objects.filter(name__contains=q)
#     else:
#         products = Product.objects.all()
#     sort_by = request.GET.get("sort", "l2h")
#     if sort_by == "l2h":
#         products = products.order_by("price")
#     elif sort_by == "h2l":
#         products = products.order_by("-price")
#     else:
#         products = products.order_by("orderitem__date_added")
#
#     brands = Product.objects.all().order_by('brandName').values('brandName').distinct()
#
#
#     context = {'products': products, 'brands': brands}
#
#     return render(request, 'store/store.html', context)


# def basket(request):
#     # request.user.customer = request.user.username
#     # print(request.user.customer)
#     # if request.user.customer.RelatedObjectDoesNotExist:
#     #     print('iofewj')
#     #     return
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#     else:
#         items = []
#         order = {'get_basket_total': 0, 'get_basket_items': 0}
#
#     context = {'items': items, 'order': order}
#     return render(request, 'store/Basket.html', context)


# def checkout(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#     else:
#         items = []
#         order = {'get_basket_total': 0, 'get_basket_items': 0}
#
#     context = {'items': items, 'order': order}
#     return render(request, 'store/Checkout3.html', context)





# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action:', action)
#     print('Product:', productId)
#
#     customer = request.user.customer
#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
#
#     orderItem.save()
#
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#
#     return JsonResponse('Item was added', safe=False)









