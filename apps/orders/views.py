import django.db.utils
from django.db import transaction
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.pay.ALI_Pay import createAliPay
from ..utils.util import checkLogin
from ..carts.models import *
from .models import *
from ..carts.serializers import *
import time
from rest_framework import mixins, generics, viewsets, status
from .serializers import *
import random
from django.db.models import Q


# Create your views here.
class PayView(APIView):
    @checkLogin
    @transaction.atomic
    def get(self, request):
        trade = request.GET.get("out_trade_no")
        params = request.GET.dict()
        sign = params.pop('sign', None)
        alipay = createAliPay()
        statu = alipay.verify(params, sign)
        if statu:
            orderObj = Orders.objects.filter(trade=trade)
            if orderObj.update(is_pay=True):
                for o in orderObj.first().items.all():
                    SecondBooks.objects.filter(id=o.goods.id).update(sold=True)
                    CartItem.objects.filter(id=o.cart_id).update(iscancel=True)
                return Response({'code': 200, 'message': '支付完成'}, status=status.HTTP_200_OK)
        return Response({'code': 400, 'error': '支付失败，请联系管理员！'}, status=status.HTTP_400_BAD_REQUEST)

    @checkLogin
    @transaction.atomic
    def post(self, request):
        carts = request.data.get('cartId')
        book = request.data.get('bookId')
        addr = request.data.get('addr')
        trade_id = time.strftime('%Y%m%d%H%M%S') + str(random.randint(0, 100))
        price = 0
        # 计算价格
        if carts:
            cartQuery = CartItem.objects.filter(id__in=carts.split('&'))
            for i in cartQuery:
                price += float(i.book.price)
        if book:
            bookObj = SecondBooks.objects.filter(id=book).first()
            price = float(bookObj.price)
        alipay = createAliPay()
        # 与后台校验价格
        if float(request.data.get('price')) == price:
            url = alipay.direct_pay(
                subject="测试订单",  # 订单名称
                # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
                out_trade_no=trade_id,  # 订单号
                total_amount=price,  # 支付金额
                return_url="http://127.0.0.1:5173/success"  # 支付成功后，跳转url
            )

            # 将前面后的支付参数，拼接到支付网关
            # 注意：下面支付网关是沙箱环境，
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

            addrObj = Address.objects.filter(id=addr).first()
            bookObj = SecondBooks.objects.filter(id=book).first()
            userObj = User.objects.filter(id=request.session.get('_auth_user_id')).first()

            # 创建订单中的购物项
            if carts:
                cartQuery = CartItem.objects.filter(id__in=carts.split('&'))
                # 创建订单
                orderObj = Orders.objects.create(trade=trade_id, price=price, address=addrObj, user=userObj)
                orderObj.save()
                for i in cartQuery:
                    OrderItemObj = OrderItems.objects.create(goods=i.book, trade=orderObj, cart=i)
                    OrderItemObj.save()
            if book:
                bookObj = SecondBooks.objects.filter(id=book).first()
                if CartItem.objects.filter(book_id=book):
                    return Response({"code": 400, 'error': '该物品已存在于购物车中！'})
                try:
                    cartObj = CartItem.objects.create(book=bookObj, user=userObj, iscancel=True)
                    cartObj.save()
                except:
                    return Response({"code": 400, 'error': '请勿重复提交！'})

                # 创建订单
                orderObj = Orders.objects.create(trade=trade_id, price=price, address=addrObj, user=userObj)
                orderObj.save()
                OrderItemObj = OrderItems.objects.create(goods=bookObj, trade=orderObj, cart=cartObj)
                OrderItemObj.save()
            return Response({'code': 200, 'redirect': re_url})
        return Response({"code": 400, 'error': '请求错误，请稍后！'})


#
# class CheckPayView(APIView):
#     def get(self, request):
#         trade = request.GET.get("trade")
#         params = request.GET.dict()
#         sign = params.pop('sign', None)
#         alipay = createAliPay()
#         statu = alipay.verify(params, sign)
#         if statu:
#             return Response({'code': 200})
#         else:
#             return Response({'code': 400})


class OrderItemsView(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    # queryset = Address.objects.filter().order_by('id')
    # serializer_class = AddressSerializers

    def list(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if id:
            ids = id.split('&')
            queryset = CartItem.objects.all().filter(id__in=ids)

            serializer = CartSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'code': 400, "error": '请刷新！'}, status=status.HTTP_400_BAD_REQUEST)


class OrdersView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrdersSerializers

    @checkLogin
    def list(self, request, *args, **kwargs):
        uid = request.session.get('_auth_user_id', None)
        queryset = self.queryset.filter(user_id=uid)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ManageOrderView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrdersSerializers
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        flag = self.queryset.filter(id=filter_kwargs['id']).update(cancel=True)
        if flag:
            return Response({'code': 200, "msg": '取消订单成功'}, status=status.HTTP_200_OK)
        return Response({'code': 400, "error": '取消订单失败！'}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self,request,*args,**kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        instance = self.queryset.filter(id=filter_kwargs['id']).first()
        if not instance.is_pay:
            alipay = createAliPay()
            # 与后台校验价格
            url = alipay.direct_pay(
                subject="测试订单",  # 订单名称
                # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
                out_trade_no=instance.trade,  # 订单号
                total_amount=float(instance.price),  # 支付金额
                return_url="http://127.0.0.1:5173/success"  # 支付成功后，跳转url
            )

            # 将前面后的支付参数，拼接到支付网关
            # 注意：下面支付网关是沙箱环境，
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
            return Response({'code': 200, 'redirect': re_url})
        return Response({"code": 400, 'error': '付款请求失败，请重试！'})


class PurchasedBooksView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrdersSerializers

    @checkLogin
    def list(self, request, *args, **kwargs):
        uid = request.session.get('_auth_user_id', None)
        queryset = self.get_queryset().filter(Q(user_id=uid) & Q(is_pay=True))

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_data(serializer))

    def get_data(self, serializer):
        data=[]
        for i in serializer.data:
            for j in i['items']:
                data.append(j['goods'])
        return data


class TransactionsView(generics.ListAPIView,generics.UpdateAPIView,generics.RetrieveAPIView):
    queryset = OrderItems.objects.filter(trade__cancel=False).order_by('-id')
    serializer_class = TradeSerializers

    @checkLogin
    def list(self, request, *args, **kwargs):
        uid = request.session.get('_auth_user_id', None)
        # queryset = self.filter_queryset(self.get_queryset().filter(user_id=31))
        queryset = self.filter_queryset(self.get_queryset().filter(goods__user_id=uid))
        serializer = self.get_serializer(queryset, many=True)
        data = list(i['trade'] for i in serializer.data)
        return Response(serializer.data)

    @checkLogin
    def update(self, request, *args, **kwargs):
        n = request.data.get('n')
        trade = request.data.get('trade')
        queryset = self.get_queryset().filter(trade=trade)

        flag = queryset.update(courier_number=n)
        if flag:
            return Response({'code': 200, 'msg': '提交快递单号信息成功'}, status=status.HTTP_200_OK)
        return Response({'code': 400, 'error': '提交快递单号信息失败'}, status=status.HTTP_400_BAD_REQUEST)

    # @checkLogin
    # def retrieve(self, request, *args, **kwargs):
    #     n = request.data.get('n')
    #     instance = self.get_queryset().filter(trade=trade)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)