from django.contrib import admin

# Register your models here.

from .models import *

# admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(ProductParametrName)
class ProductParametrNameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('product',)

@admin.register(ProductParametrValue)
class ProductParametrValueAdmin(admin.ModelAdmin):
    autocomplete_fields = ('parameter_name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'product', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


