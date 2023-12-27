from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from .models import *


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'is_superuser',
        'last_login',
        'avatar'
    )

    list_display_links = (
        'id',
        'username',
        'email',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'gender', 'phone', 'sendaddress',
                           'signature', 'province', 'city', 'county')}),

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')})
    )

    ordering = ('id',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user',
        'name',
        'phone',
        'get_total_address',
        'default',
    )

    list_display_links = (
        'id',
        'get_user',
    )

    def get_user(self, obj):
        return obj.user.username

    def get_total_address(self, obj):
        return obj.region + obj.address

    get_user.short_description = '所属用户'
    get_total_address.short_description = '详情地址'
