from django.db import models
from django.db.models import Avg, Max, Min, Count, Sum
from apps.utils.image_storage import ImageStorage
from apps.users.models import User


# Create your models here.


class CategoryFirst(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='类名', unique=True)

    class Meta:
        verbose_name = '一级类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @staticmethod
    def get_category_second(category_id):
        return CategoryFirst.objects.get(id=category_id)


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        CategoryFirst,
        related_name='books',
        on_delete=models.RESTRICT,
        verbose_name='类别')
    name = models.CharField(max_length=50, verbose_name='书名')
    isbn = models.CharField(max_length=13, verbose_name='ISBN', db_index=True, unique=True)
    image = models.ImageField(
        upload_to='books/%Y/%m/', storage=ImageStorage(), verbose_name='封面')
    author = models.CharField(max_length=50, verbose_name='作者')
    translator = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='译者')
    press = models.CharField(max_length=50, verbose_name='出版社', blank=True, null=True)
    revision = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='版次')
    published_date = models.DateField(verbose_name='出版年月', blank=True, null=True)
    page_numbers = models.PositiveSmallIntegerField(verbose_name='页数', blank=True, null=True)
    describe = models.CharField(max_length=1024, verbose_name='简介', blank=True, null=True)
    author_brief = models.CharField(max_length=1024, verbose_name='作者简介', blank=True, null=True)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='原价')

    # stock = models.PositiveIntegerField(verbose_name='存货量')
    # sales = models.PositiveIntegerField(verbose_name='销售量')

    class Meta:
        verbose_name = '原书信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @staticmethod
    def get_hot_books():
        second_books_set = SecondBooks.objects.filter(sold=False,returns=False,transit=False).values(
            "originbook").annotate(ob_count=Count('originbook')).order_by('-ob_count')

        origin_book_id_list = [i['originbook'] for i in second_books_set]
        origin_book_set = Books.objects.filter(id__in=origin_book_id_list)
        return origin_book_set

    @staticmethod
    def get_start_price(obj):
        min_price = SecondBooks.objects.filter(originbook__id=obj['id']).aggregate(min=Min("price"))['min']
        return "%.2f" % min_price if min_price else 0

    @staticmethod
    def get_new_message(obj):
        return SecondBooks.objects.filter(originbook__id=obj['id']).order_by("ptime").first()


class SecondBooks(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        related_name='sellbooks',
        on_delete=models.CASCADE,
        verbose_name='发售人'
    )
    name = models.CharField(max_length=50, verbose_name='书名')
    image = models.ImageField(
        upload_to='books/%Y/%m/', storage=ImageStorage(), verbose_name='封面')
    originbook = models.ForeignKey(
        Books,
        related_name='secondhandbooks',
        on_delete=models.PROTECT,
        verbose_name='原书'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='二手价')
    sold = models.BooleanField(default=False, verbose_name='是否售出')
    transit = models.BooleanField(default=False, verbose_name='运输中')
    returns = models.BooleanField(default=False, verbose_name='是否退货')
    ptime = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    remove = models.BooleanField(default=False, verbose_name='是否下架')

    class Meta:
        verbose_name = '二手图书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
