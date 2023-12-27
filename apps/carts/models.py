from django.db import models
from apps.users.models import User
from apps.books.models import SecondBooks
import django.utils.timezone as timezone


# Create your models here.


# class Cart(models.Model):
#     id = models.AutoField(primary_key=True)
#
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = '购物车'
#         verbose_name_plural = verbose_name


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(
        SecondBooks,
        related_name='item',
        on_delete=models.CASCADE,
        verbose_name='图书'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='所属用户',
    )
    storagetime = models.DateTimeField(
        default=timezone.now,
        verbose_name='入库时间'
    )
    iscancel = models.BooleanField(default=False,verbose_name='已删除')

    class Meta:
        verbose_name = '购物项'
        verbose_name_plural = verbose_name
        unique_together = ['book','user']

    def __str__(self):
        return self.book.name
