from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'isbn',
        'author',
        'press',
        'original_price',
        # 'stock',
        # 'sales',
    )

    list_display_links = (
        'name',
        'isbn',
    )

@admin.register(SecondBooks)
class SecondBooksAdmin(admin.ModelAdmin):
    list_display = (
        'get_isbn',
        'get_origin_name',
        'name',
        'get_sell_user',
        'price'
    )

    list_display_links = (
        'get_isbn',
        'get_origin_name',
        'name',
    )

    def get_origin_name(self,obj):
        return obj.originbook.name

    def get_isbn(self,obj):
        return obj.originbook.isbn

    def get_sell_user(self,obj):
        return obj.user.username

    get_origin_name.short_description = '原书名'
    get_isbn.short_description = 'ISBN'
    get_sell_user.short_description = '发售人'


@admin.register(CategoryFirst)
class CategoryFirstAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )