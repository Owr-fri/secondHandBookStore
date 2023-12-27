from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.callExpressRequest import getShippingCost
from .models import *
from .serializers import *


# Create your views here.
class CarouselView(generics.ListAPIView,
                   generics.GenericAPIView):
    queryset = Carousel.get_carousels()
    serializer_class = CarouselSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# 运费API
class ShippingFeeView(APIView):
    def get(self, request):
        msgData = {
            "sendProvince": request.GET.get("sendProvince"),
            "sendCity": request.GET.get("sendCity"),
            "sendCounty": request.GET.get("sendCounty"),
            "deliveryProvince": request.GET.get("deliveryProvince"),
            "deliveryCity": request.GET.get("deliveryCity"),
            "deliveryCounty": request.GET.get("deliveryCounty"),
            "weight": request.GET.get("weight"),
        }
        data = getShippingCost(msgData=str(msgData))
        return Response(data=data)