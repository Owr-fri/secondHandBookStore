import time

from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..users.serializers import UserSerializers
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
from ..utils.util import checkLogin, reformUserInfo


class FilterListModelMixin(generics.GenericAPIView):
    def get_data(self, serializer):
        return serializer.data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.get_data(serializer))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   generics.GenericAPIView):
    queryset = CategoryFirst.objects.all().order_by('id')
    serializer_class = CategoryFirstSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HotBooksView(generics.ListAPIView):
    queryset = Books.get_hot_books().order_by('id')
    serializer_class = BooksSerializer

    def get_data(self, serializer):
        data = []
        for ser in serializer.data:
            data.append({
                'id': ser['id'],
                'name': ser['name'],
                'image': ser['image'],
                'author': ser['author'],
                'translator': ser['translator'],
                'describe': ser['describe'],
                # 'origin_price': ser['original_price'],
                'start_price': "%.02f" % float(Books.get_start_price(ser))
            })
        return data

    def list(self, request, *args, **kwargs):
        all = request.GET.get("all", None)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None and all is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(self.get_data(serializer))
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_data(serializer)[:10])


class SearchBooksView(FilterListModelMixin,
                      generics.GenericAPIView):
    queryset = SecondBooks.objects.all().order_by('id')
    serializer_class = SecondBooksSerializer

    def get_queryset(self):
        search_key = self.request.query_params.get('search_key')
        queryset = SecondBooks.objects.filter(id=-1)
        if SecondBooks.objects.filter(originbook__isbn=search_key):
            queryset = SecondBooks.objects.filter(originbook__isbn=search_key)
        elif SecondBooks.objects.filter(originbook__author__contains=search_key):
            queryset = SecondBooks.objects.filter(originbook__author__contains=search_key)
        elif SecondBooks.objects.filter(originbook__name__contains=search_key):
            queryset = SecondBooks.objects.filter(originbook__name__contains=search_key)
        return queryset.order_by('id')

    def get_data(self, serializer):
        data = []
        for ser in serializer.data:
            data.append({
                'id': ser['id'],
                'name': ser['name'],
                'image': ser['image'],
                'price': ser['price'],
                'user': ser['user'],
            })
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookCategoryByIdView(FilterListModelMixin,
                           generics.GenericAPIView):
    queryset = CategoryFirst.objects.all().order_by('id')
    serializer_class = BooksSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(id=self.kwargs[self.lookup_field]).first().books.all().order_by('id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.get_data(serializer))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_data(self, serializer):
        data = []
        for ser in serializer.data:
            data.append({
                'id': ser['id'],
                'name': ser['name'],
                'image': ser['image'],
                'original_price': ser['original_price'],
                'author': ser['author'],
                'describe': ser['describe'],
            })
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SecondBookListView(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):
    queryset = Books.objects.all().order_by('id')
    serializer_class = SecondBooksSerializer
    origin_book_serializer_class = BooksSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        originBook = self.origin_book_serializer_class(instance)
        bookList = instance.secondhandbooks.filter(Q(returns=0) & Q(sold=0) & Q(transit=0) & Q(remove=0)).order_by('id')

        orderKey = request.GET.get('byOrder')

        if orderKey == 'price':
            bookList = bookList.order_by('price')
        if orderKey == '-price':
            bookList = bookList.order_by('-price')
        if orderKey == 'new':
            bookList = bookList.order_by('-ptime')

        serializer = self.get_serializer(bookList, many=True)

        page = self.paginate_queryset(bookList)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'originBook': originBook.data,
                'bookList': self.get_data(serializer)
            })

        serializer = self.get_serializer(bookList, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_data(self, serializer):
        data = []
        for ser in serializer.data:
            data.append({
                'id': ser['id'],
                'name': ser['name'],
                'image': ser['image'],
                'user_name': ser['user_name'],
                'user_id': ser['user'],
                'price': ser['price'],
            })
        return data


def get_data(serializer, *args):
    ser = serializer.data
    origin_book = args[0]
    user = args[1]
    return dict(id=ser['id'], name=ser['name'], image=ser['image'], price=ser['price'], originbook={
        'id': origin_book['id'],
        'category_name': origin_book['category_name'],
        'name': origin_book['name'],
        'image': origin_book['image'],
        'author': origin_book['author'],
        'translator': origin_book['translator'],
        'press': origin_book['press'],
        'revision': origin_book['revision'],
        'published_date': origin_book['published_date'][:7],
        'page_numbers': origin_book['page_numbers'],
        'describe': origin_book['describe'],
        'isbn': origin_book['isbn'],
        'original_price': origin_book['original_price'],
        'author_brief': origin_book['author_brief']
    }, ptime=ser['ptime'][:10], user=reformUserInfo(user))


class SecondBookView(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     generics.GenericAPIView):
    queryset = SecondBooks.objects.all().order_by('id')
    serializer_class = SecondBooksSerializer
    origin_book_serializer_class = BooksSerializer
    user_serializer_class = UserSerializers
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        origin_book_data = self.origin_book_serializer_class(instance.originbook).data
        user_data = self.user_serializer_class(instance.user).data
        serializer = self.get_serializer(instance)
        return Response(get_data(serializer, origin_book_data, user_data))

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CategoryBookView(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = CategoryFirst.objects.all().order_by('id')
    serializer_class = CategoryBookSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        page = self.paginate_queryset(self.get_data(serializer))
        if page is not None:
            return self.get_paginated_response(page)

        return Response(self.get_data(serializer))

    def get_data(self, serializer):
        data = []
        for ser in serializer.data['books']:
            message = Books.get_new_message(ser)
            messageSer = SecondBooksSerializer(message).data
            min_price = Books.get_start_price(ser)
            data.append({
                'id': ser['id'],
                'name': ser['name'],
                'image': ser['image'],
                'isbn': ser['isbn'],
                'author': ser['author'],
                'translator': ser['translator'],
                'press': ser['press'],
                'revision': ser['revision'],
                'original_price': ser['original_price'],
                'published_date': "-".join(ser['published_date'].split("-")[:-1]) if ser['published_date'] else '',
                'min_price': min_price,
                'messageInfo': {
                    'id': messageSer['id'],
                    'user_name': messageSer['user_name'],
                    'ptime': messageSer['ptime'].replace('T', ' ').split('.')[0] if messageSer['ptime'] else messageSer[
                        'ptime'],
                } if message else "",
            })
        return data


class BookSearchView(generics.ListAPIView):
    queryset = Books.objects.all().order_by('id')
    serializer_class = BooksSerializer

    def list(self, request, *args, **kwargs):
        key = request.GET.get('key')
        queryset = self.queryset.filter(Q(isbn__icontains=key) | Q(name__icontains=key) | Q(author__icontains=key))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.get_data(serializer))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_data(self, serializer):
        data = []
        for ser in serializer.data:
            ser['min_price'] = Books.get_start_price(ser)
            ser['count'] = SecondBooks.objects.filter(Q(originbook__id=ser['id']) & Q(returns=False) & Q(sold=False)
                                                      & Q(transit=False)).count()
            data.append(ser)
        return data


class SearchBooksByNameView(generics.ListAPIView):
    queryset = Books.objects.all().order_by('id')
    serializer_class = BooksSerializer

    def list(self, request, *args, **kwargs):
        key = request.GET.get('key')
        queryset = self.queryset.filter(name__icontains=key)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SearchCategoryView(generics.ListAPIView):
    queryset = CategoryFirst.objects.all().order_by('id')
    serializer_class = CategoryFirstSerializer

    def list(self, request, *args, **kwargs):
        key = request.GET.get('key')
        queryset = self.queryset.filter(name__icontains=key)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OriginBookInfoView(generics.UpdateAPIView, generics.CreateAPIView):
    queryset = Books.objects.all().order_by('id')
    serializer_class = BooksSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if data['imgFile']:
            path = ImageStorage()._save(f'books/{time.strftime("%Y")}/{time.strftime("%m")}/' + data['imgFile'].name
                                        , data['imgFile'])
            data['image'] = path

        if data['updateCategory']:
            cid = CategoryFirst.objects.create(name=data['updateCategory'])
            data['category'] = CategoryFirst.objects.filter(id=cid.id).first()

        else:
            data['category'] = CategoryFirst.objects.filter(id=data['category']).first()

        # del data['category_name']
        del data['imgFile']
        del data['updateCategory']

        temp = {
            i: data[i] for i in data
        }
        bid = Books.objects.create(**temp)
        if bid:
            return Response({'code': 200, 'msg': '新增成功','data':{'id':bid.id}}, status=status.HTTP_201_CREATED)
        return Response({'code': 400, 'msg': '新增失败'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()

        instance = self.queryset.filter(id=data['id'])
        if data['imgFile']:
            path = ImageStorage()._save(f'books/{time.strftime("%Y")}/{time.strftime("%m")}/' + data['imgFile'].name
                                        , data['imgFile'])
            instance.update(image=path)

        if data['updateCategory']:
            cid = CategoryFirst.objects.create(name=data['updateCategory'])
            data['category'] = cid

        # 删除多余信息
        del data['image']
        del data['imgFile']
        del data['category_name']
        del data['updateCategory']
        temp = {
            i: data[i] for i in data
        }
        flag = instance.update(**temp)
        if flag:
            return Response({'code': 200, 'msg': '保存成功'}, status=status.HTTP_200_OK)
        return Response({'code': 400, 'msg': '保存失败'}, status=status.HTTP_400_BAD_REQUEST)


class SecondBookInfoView(generics.CreateAPIView, generics.ListAPIView,
                         generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = SecondBooks.objects.all().order_by('id')
    serializer_class = SecondBooksSerializer

    @checkLogin
    def create(self, request, *args, **kwargs):
        data = request.data
        # 下载图片
        path = ImageStorage()._save(f'books/{time.strftime("%Y")}/{time.strftime("%m")}/' + data['image'].name
                                    , data['image'])
        data['image'] = path
        # 获取原书信息
        data['originbook'] = Books.objects.filter(id=data['originbook']).first()
        # 获取用户id
        data['user_id'] = request.session.get('_auth_user_id', None)
        user = User.objects.filter(id=data['user_id']).first()
        if not user.phone:
            return Response({'code': 400, 'error': '请先绑定手机号'}, status=status.HTTP_400_BAD_REQUEST)
        temp = {
            i: data[i] for i in data
        }
        bid = SecondBooks.objects.create(**temp)
        if bid:
            return Response({'code': 200, 'msg': '保存成功'}, status=status.HTTP_201_CREATED)
        return Response({'code': 400, 'error': '保存失败'}, status=status.HTTP_400_BAD_REQUEST)

    @checkLogin
    def list(self, request, *args, **kwargs):
        uid = request.session.get('_auth_user_id', None)
        queryset = self.filter_queryset(self.get_queryset().filter(user_id=uid))

        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 200, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    @checkLogin
    def destroy(self, request, *args, **kwargs):
        bid = request.GET.get('bid')
        instance = self.queryset.filter(id=bid)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @checkLogin
    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        bid = request.data.get('id')

        instance = SecondBooks.objects.filter(id=bid)
        if data['imgFile']:
            path = ImageStorage()._save(f'books/{time.strftime("%Y")}/{time.strftime("%m")}/' + data['imgFile'].name
                                        , data['imgFile'])
            instance.update(image=path)

        # 删除多余信息
        del data['image']
        del data['imgFile']
        del data['user_name']
        del data['originbook']
        temp = {
            i: data[i] for i in data
        }
        for i in ['returns', 'sold', 'transit', 'remove']:
            temp[i] = True if temp[i] == 'true' else False
        print(temp)
        flag = instance.update(**temp)
        if flag:
            return Response({'code': 200, 'msg': '保存成功'}, status=status.HTTP_200_OK)
        return Response({'code': 400, 'error': '保存失败'}, status=status.HTTP_400_BAD_REQUEST)


class AllByIdView(APIView):
    def get(self, request):
        uid = request.GET.get("u")
        books = SecondBooks.objects.filter(user_id=uid)
        user = User.objects.filter(id=uid).first()
        user_data = UserSerializers(user).data
        books_data = SecondBooksSerializer(books, many=True).data
        data = dict(books=books_data, user=reformUserInfo(user_data))
        return Response(data, status=status.HTTP_202_ACCEPTED)
