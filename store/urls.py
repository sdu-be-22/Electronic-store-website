from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name="store"),
  path('shop/', views.shop, name="shop"),
  path('checkout/', views.checkout, name="checkout"),
  path('cart/', views.cart, name="cart"),
  path('update_item/', views.updateItem, name="update_item"),

  path('smartphones/', views.smartphones, name="smartphones"),
  path('laptops/', views.laptops, name='laptops'),
  path('cameras/', views.cameras, name='cameras'),
  path('accounts/registration/', views.register, name='register'),
  path('', views.index, name='home'),
  path('shop/products/<int:myid>', views.productView, name="productView"),








  # path('brands/<str:brandName>', views.brandView, name="brandView"),

  # kjdijewiojdoweji
  # path('', views.store, name="store"),
  # path('basket/', views.basket, name="basket"),
  # path('checkout/', views.sendMail, name="sendMail"),
  # path('smartphones/', views.smartphones, name="smartphones"),
  # path('laptops/', views.laptops, name='laptops'),
  # path('cameras/', views.cameras, name='cameras'),
  #
  # path('update_item/', views.updateItem, name="update_item"),
  #
  # path('accounts/registration/', views.register, name='register'),
  # path('', views.home, name='home'),
  #
  # path('products/', views.ProductList.as_view()),
  # path('products/<int:myid>', views.productView, name="productView"),
  # path('brands/<str:brandName>', views.brandView, name="brandView"),

  # fnkejwfio
  # path('history/', views.history, name="history"),
]