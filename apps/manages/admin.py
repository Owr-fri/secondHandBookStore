from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image',
        'content',
        'added_time'
    )

    ordering = (
        'id',
    )
