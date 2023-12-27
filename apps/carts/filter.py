import django_filters
from .models import *


class CartItemFilter(django_filters.FilterSet):
    class META:
        model = CartItem
        fields = ['iscancel']