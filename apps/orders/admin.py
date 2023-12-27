from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'trade',
        'user',
        'price',
        'is_pay',
        'cancel',
    )
    list_display_links = (
        'id',
        'trade',
        'user',
    )


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'trade',
        'goods',
    )
    list_display_links = (
        'id',
        'trade',
    )
