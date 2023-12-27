from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from .models import *
from .filter import *
from .serializers import *
from ..books.models import SecondBooks
from ..utils.util import checkLogin


# Create your views here.
class CartItemView(generics.GenericAPIView,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = CartItem.objects.filter(iscancel=False)
    serializer_class = CartItemSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        book_id = self.kwargs[self.lookup_field]
        user_id = request.session.get('_auth_user_id', None)
        if user_id:
            book_user_id = SecondBooks.objects.filter(id=book_id).first().user_id
            if int(user_id) == book_user_id:
                return Response({'error': '请勿添加自己的商品', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data={"book": book_id, "user": user_id})
            if not serializer.is_valid():
                return Response({'error': '请勿重复添加商品', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'msg': '添加成功', 'code': 201}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': '请先登录', 'code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'msg': "删除成功", 'code': 200}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CartView(mixins.DestroyModelMixin, generics.ListAPIView):
    queryset = CartItem.objects.filter(iscancel=False)
    serializer_class = CartSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('user_id',)
    ordering = ['-storagetime']

    def list(self, request, *args, **kwargs):
        user_id = request.session.get('_auth_user_id', None)
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=user_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @checkLogin
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        selected = request.data
        for i in selected:
            instance = self.get_cart_item(i)
            self.perform_destroy(instance)
        return Response({'msg': "删除成功", 'code': 200}, status=status.HTTP_200_OK)

    def get_cart_item(self, cartId):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'id': cartId}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
