# from importlib.resources import _

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    SM = 'Smartphones'
    LT = 'Laptops'
    CM = 'Cameras'
    WT = 'Watch'
    typesOfProducts = [
        ('Smartphones', 'Smartphones'),
        (LT, 'Laptops'),
        (CM, 'Cameras'),
        (WT, 'Watch')
    ]
    prTypes = models.CharField(("Product type"), max_length=50, choices=typesOfProducts, blank=True)
    name = models.CharField(max_length=200)
    brandName = models.CharField(max_length=200)

    price = models.FloatField(max_length=140)
    # digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=1000, default="")

    # characteristic = models.CharField(max_length=500)
    # brand = models.CharField(max_length=50)
    last_visit = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ProductParametrName(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='parameter_names')
    name = models.CharField(max_length=200)

    def str(self):
        return ("%s %s") % (self.product.name, self.name)


class ProductParametrValue(models.Model):
    parameter_name = models.OneToOneField(ProductParametrName, null=True, blank=True, on_delete=models.CASCADE,
                                          related_name='parameter_value')
    name = models.CharField(max_length=200)

    def str(self):
        return ("%s %s %s") % (self.parameter_name.product.name, self.parameter_name.name, self.name)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_basket_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_basket_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
