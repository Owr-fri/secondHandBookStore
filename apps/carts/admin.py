from django.contrib import admin
from . import models

# Register your models here.
# @admin.register(models.Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#     )
#
#     ordering = (
#         'user',
#     )
#
#     search_fields = (
#         'user',
#     )

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'get_book',
        'get_cart',
        'storagetime',
    )

    list_display_links = (
        'get_cart',
        'get_book'
    )

    def get_book(self,obj):
        return obj.book.name

    def get_cart(self,obj):
        return obj.cart.user

    get_book.short_description = '书名'
    get_cart.short_description = '购物车所属'
