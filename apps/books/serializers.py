from .models import *
from rest_framework import serializers


class BooksSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Books
        fields = '__all__'


class CategoryFirstSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryFirst
        fields = ('id', 'name')


class CategoryBookSerializer(serializers.ModelSerializer):
    books = BooksSerializer(many=True)

    class Meta:
        model = CategoryFirst
        fields = '__all__'


class SecondBooksSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = SecondBooks
        fields = '__all__'


class SecondBooksAndUserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = SecondBooks
        fields = '__all__'


class CartSecondBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondBooks
        fields = ('id', 'name', 'image', 'price')


class OrderSecondBookSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name')

    class Meta:
        model = SecondBooks
        fields = ('id', 'name', 'image', 'price', 'user')
