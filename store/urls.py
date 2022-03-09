from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('basket/', views.basket, name="basket"),
	path('checkout/', views.checkout, name="checkout"),
	path('smartphones/', views.smartphones, name="smartphones"),
	path('laptops/', views.laptops, name='laptops'),
	path('cameras/', views.cameras, name='cameras'),

	path('update_item/', views.updateItem, name="update_item"),
]
