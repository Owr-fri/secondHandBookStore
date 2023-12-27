from .models import *
from rest_framework import serializers
from ..books.serializers import *
from ..users.serializers import *


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    book = CartSecondBookSerializer()
    user_name = serializers.CharField(source='book.user.first_name')
    dianpu_id = serializers.CharField(source='book.user.id')

    class Meta:
        model = CartItem
        exclude = ('iscancel', 'storagetime', 'user')


class CartToOrderSerializer(serializers.ModelSerializer):
    book = CartSecondBookSerializer()
    user_name = serializers.CharField(source='book.user.first_name')
    dianpu_id = serializers.CharField(source='book.user.id')

    class Meta:
        model = CartItem
        exclude = ('iscancel', 'storagetime', 'user')
