from django.db import models
from django.db.models import Avg, Max, Min, Count, Sum
from apps.users.models import User, Address
from apps.books.models import SecondBooks
from apps.carts.models import CartItem


# Create your models here.

class Orders(models.Model):
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.trade

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,
                             related_name='orders',
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    trade = models.CharField(verbose_name='订单号', db_index=True, unique=True, max_length=20)
    address = models.ForeignKey(Address,
                                related_name='orders',
                                on_delete=models.CASCADE,
                                verbose_name='地址', )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='订单价格')
    is_pay = models.BooleanField(verbose_name='已支付', default=False)
    cancel = models.BooleanField(verbose_name='已取消', default=False)


class OrderItems(models.Model):
    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

    id = models.AutoField(primary_key=True)
    trade = models.ForeignKey(Orders,
                              related_name='items',
                              on_delete=models.CASCADE,
                              to_field='trade',
                              verbose_name='订单号')
    goods = models.ForeignKey(SecondBooks,
                              related_name='orders',
                              on_delete=models.DO_NOTHING,
                              verbose_name='商品')
    cart = models.ForeignKey(CartItem,
                             related_name='order',
                             on_delete=models.DO_NOTHING,
                             verbose_name='购物车单项')
    courier_number = models.CharField(verbose_name='快递单号', max_length=50, null=True)
