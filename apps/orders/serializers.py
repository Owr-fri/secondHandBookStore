from .models import *
from rest_framework import serializers
from ..users.serializers import AddressSerializers, CartUserSerializer
from ..books.serializers import OrderSecondBookSerializer
from ..orders.models import Orders


class OrderItemsSerializers(serializers.ModelSerializer):
    goods = OrderSecondBookSerializer()

    class Meta:
        model = OrderItems
        fields = '__all__'


class OrdersSerializers(serializers.ModelSerializer):
    items = OrderItemsSerializers(many=True)
    address = AddressSerializers()
    user = CartUserSerializer()

    class Meta:
        model = Orders
        fields = '__all__'


class simpleOrderSerializers(serializers.ModelSerializer):
    address = AddressSerializers()
    num = serializers.CharField(source='trade')

    class Meta:
        model = Orders
        fields = ('address', 'is_pay', 'price', 'num')


class TradeSerializers(serializers.ModelSerializer):
    trade = simpleOrderSerializers()
    goods = OrderSecondBookSerializer()

    class Meta:
        model = OrderItems
        fields = ('trade', 'goods')
