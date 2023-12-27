from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.CartItemView.as_view()),
    path('', views.CartView.as_view())
]
