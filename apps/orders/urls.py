from django.urls import path
from . import views

# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('pay/', views.PayView.as_view()),
    # path('check/',views.CheckPayView.as_view())
    path("items/", views.OrderItemsView.as_view()),
    path("", views.OrdersView.as_view()),
    path("<int:id>/", views.ManageOrderView.as_view()),
    # 已购书籍
    path("purchasedBooks/", views.PurchasedBooksView.as_view()),
    # 快递
    path('transactions/',views.TransactionsView.as_view())
]
