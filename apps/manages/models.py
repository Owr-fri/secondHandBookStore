from django.db import models
from apps.utils.image_storage import ImageStorage

# Create your models here.
class Carousel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to='carousel/%Y/%m', storage=ImageStorage(), verbose_name='轮播')
    content = models.CharField(max_length=20, verbose_name='图片内容')
    added_time = models.DateTimeField(auto_now=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    @staticmethod
    def get_carousels(number=4):
        return Carousel.objects.order_by('-added_time').all()[:number]