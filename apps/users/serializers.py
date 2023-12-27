from .models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password', 'groups', 'is_active', 'is_staff', 'is_superuser', 'user_permissions')

    # password = serializers.CharField(read_only=True, required=False)
    username = serializers.CharField(read_only=True, required=False)


class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name')


class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = '__all__'
        exclude = ('zip_code',)
