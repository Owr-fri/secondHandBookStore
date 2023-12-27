from django.db import models
from apps.utils.image_storage import ImageStorage
from django.contrib.auth.models import AbstractUser

# Create your models here.
sex_choice = (
    (0, '女性'),
    (1, '男性'),
)


class User(AbstractUser):
    nickname = models.CharField(max_length=8, verbose_name='昵称',null=True, blank=True,)
    avatar = models.ImageField(
        upload_to='avatar/%Y/%m',
        storage=ImageStorage(),
        default='avatar/default.jpg',
        verbose_name='头像')

    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    sendaddress = models.CharField(max_length=50, null=True, blank=True, verbose_name='发货地址')
    province = models.CharField(max_length=15, null=True, blank=True, verbose_name='省份')
    city = models.CharField(max_length=15, null=True, blank=True, verbose_name='市')
    county = models.CharField(max_length=15, null=True, blank=True, verbose_name='区')
    gender = models.IntegerField(choices=sex_choice, default=1, verbose_name='性别')
    signature = models.CharField(max_length=80, null=True, blank=True, verbose_name='个性签名')

    class Meta:
        # app_label = ''
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # def create_cart(self):
    #     from apps.carts.models import Cart
    #     cart = Cart()
    #     cart.user = self
    #     cart.save()


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        related_name='address',
        on_delete=models.CASCADE,
        verbose_name='所属用户', )
    name = models.CharField(max_length=25, verbose_name='收货人姓名')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    # region = models.CharField(max_length=50, verbose_name='地址信息')
    province = models.CharField(max_length=15, verbose_name='省份')
    city = models.CharField(max_length=15,  verbose_name='市')
    county = models.CharField(max_length=15, verbose_name='区')
    address = models.CharField(max_length=100, verbose_name='详细地址')
    total_address = models.CharField(max_length=100, verbose_name='完整地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮编编码', blank=True, null=True)
    default = models.BooleanField(default=False, verbose_name='默认收货地址')

    class Meta:
        verbose_name = '收货人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
