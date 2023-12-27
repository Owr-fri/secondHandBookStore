import re
import time
import json

from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from ..carts.models import *
from rest_framework import mixins, generics, viewsets
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from ..carts.serializers import CartSerializer
from ..utils.image_storage import ImageStorage
from ..utils.util import checkLogin


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')

        # 校验数据
        # 1、校验参数不能为空
        if not all([name, password, password_confirmation]):
            return Response({'error': '所有参数均不能为空', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2、校验用户名是否被使用
        if User.objects.filter(username=email).exists():
            return Response({'error': '用户名已经被使用', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 3、两次密码必须一致
        if password != password_confirmation:
            return Response({'error': '两次密码必须一致', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 4、校验密码长度
        if not (6 <= len(password) <= 18):
            return Response({'error': '密码长度必须在6到18位之间', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 5、校验邮箱是否被使用
        if User.objects.filter(email=email).exists():
            return Response({'error': '邮箱已经被使用', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 6、邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': '邮箱格式不正确', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 所有数据验证通过就创建用户
        obj = User.objects.create_user(username=email, password=password, email=email, first_name=name)

        return Response({'message': '创建成功', "code": "200"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        if not all([username, password]):
            return Response({'error': '所有参数均不能为空', 'code': '422'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serializer = UserSerializers(user)
                info = {
                    "email": serializer.data['email'],
                    'name': serializer.data['first_name'],
                    'avatar': serializer.data['avatar'],
                }
                return Response({'message': '登录成功', 'code': '200', 'info': info}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '用户尚未激活', 'code': '403'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': '用户名或密码错误', 'code': '422'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CheckView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        userId = request.session.get('_auth_user_id', None)
        if userId == id:
            return Response({'error': '请勿购买自己的商品！', 'code': '403'}, status=status.HTTP_403_FORBIDDEN)
        if userId:
            return Response({'tag': True, 'code': '200'}, status=status.HTTP_200_OK)
        else:
            return Response({'tag': False, 'code': '401'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': '退出成功', 'code': '200'}, status=status.HTTP_200_OK)


class InfoView(generics.GenericAPIView,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers

    def get_data(self, serializer):
        ser = serializer.data
        data = {
            'id': ser['id'],
            'avatar': ser['avatar'],
            'last_login': ser['last_login'][:19].replace('T', ' '),
            'name': ser['first_name'],
            'nickname': ser['nickname'],
            'gender': ser['gender'],
            # 'describe': ser['describe'],
            'sendaddress': ser['sendaddress'],
            'username': ser['username'],
            'signature': ser['signature'] if ser['signature'] else '',
            'province': ser['province'],
            'county': ser['county'],
            'city': ser['city'],
        }
        return data

    @checkLogin
    def retrieve(self, request, *args, **kwargs):
        userId = request.session.get('_auth_user_id', None)
        instance = self.queryset.get(id=userId)
        serializer = self.get_serializer(instance)
        return Response(self.get_data(serializer), status=status.HTTP_200_OK)

    @checkLogin
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        userId = request.session.get('_auth_user_id', None)
        instance = self.queryset.get(id=userId)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({'msg': '保存成功', 'code': 200}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)


class NicknameView(generics.GenericAPIView,
                   mixins.UpdateModelMixin):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers

    @checkLogin
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        userId = request.session.get('_auth_user_id', None)
        instance = self.queryset.get(id=userId)

        if not request.data['nickName']:
            return Response({'error': '昵称不能为空', 'code': 422}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data={"nickname": request.data['nickName']}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'msg': '昵称修改成功', 'code': 200}, status=status.HTTP_200_OK)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)


class AvatarView(generics.GenericAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers

    def post(self, request):
        avatarImg = request.FILES.get('file')
        userId = request.session.get('_auth_user_id', None)
        if userId:
            path = ImageStorage()._save(f'avatar/{time.strftime("%Y")}/{time.strftime("%m")}/' + avatarImg.name
                                        , avatarImg)
            flag = User.objects.filter(id=userId).update(avatar=path)
            instance = User.objects.filter(id=userId).first()
            serializer = self.get_serializer(instance)
            currentAvatar = serializer.data['avatar']
            shotURL = self.serializer_class(instance).data['avatar']
            if flag:
                return Response({"msg": "图片上传成功", "code": 200, "avatar": currentAvatar, 'shotURL': shotURL},
                                status=status.HTTP_200_OK)
            else:
                return Response({"msg": "图片上传失败", "code": 400}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': '用户未登录', 'code': 401}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordView(generics.GenericAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers

    @checkLogin
    def put(self, request, *args, **kwargs):
        newPwd = request.data.get('new')
        oldPwd = request.data.get("old")

        userId = request.session.get('_auth_user_id', None)
        instance = User.objects.filter(id=userId).first()

        if not all([newPwd, oldPwd]):
            return Response({'error': '所有参数均不能为空', 'code': '422'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if newPwd == oldPwd:
            return Response({'error': '设置的新密码不可以和最近使用的一样', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        if not (6 <= len(newPwd) <= 18):
            return Response({'error': '密码长度必须在6到18位之间', "code": "422"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        is_true_password = check_password(oldPwd, instance.password)
        if not is_true_password:
            return Response({'error': '当前密码输入不正确', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

        instance.set_password(newPwd)
        instance.save()

        return Response({'msg': '密码修改成功', 'code': 200}, status=status.HTTP_200_OK)


class NameView(generics.GenericAPIView,
               mixins.UpdateModelMixin):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers

    @checkLogin
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        userId = request.session.get('_auth_user_id', None)
        instance = self.queryset.get(id=userId)

        if not request.data['name']:
            return Response({'error': '显示名不能为空', 'code': 422}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data={"first_name": request.data['name']}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'msg': '显示名修改成功', 'code': 200}, status=status.HTTP_200_OK)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)


class AddressView(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Address.objects.filter().order_by('id')
    serializer_class = AddressSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @checkLogin
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @checkLogin
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data.get("addressInform")
        data['user'] = request.session.get('_auth_user_id', None)
        data['total_address'] += " " + data['address']
        instance = self.queryset.filter(id=request.data.get("id", None)).first()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if data['default']:
            self.queryset.filter(user_id=request.session.get('_auth_user_id', None)).update(default=False)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'code': 200, "data": serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=request.session.get('_auth_user_id', None))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.get("addressInform")
        data['user'] = request.session.get('_auth_user_id', None)
        data['total_address'] += " " + data['address']
        if self.queryset.filter(user_id=request.session.get('_auth_user_id', None)).count() >= 5:
            return Response({'error': '地址不超过五条', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        if data['default']:
            self.queryset.filter(user_id=request.session.get('_auth_user_id', None)).update(default=False)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'code': 200, "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        addrId = request.GET.get('id')
        instance = Address.objects.filter(id=addrId).first()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhoneView(APIView):
    @checkLogin
    def post(self, request):
        phone = request.data.get('phone')
        print(phone)
        flag = User.objects.filter(id=request.session.get('_auth_user_id', None)).update(phone=phone)
        if flag:
            return Response({'code': 200, 'msg': '保存成功'}, status=status.HTTP_200_OK)
        return Response({'code': 400, 'msg': '保存失败'}, status=status.HTTP_400_BAD_REQUEST)