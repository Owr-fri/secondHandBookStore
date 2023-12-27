from django.urls import path
from . import views

# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/<int:id>/', views.BookCategoryByIdView.as_view()),
    path('hot_books/', views.HotBooksView.as_view()),
    path('search_books/', views.SearchBooksView.as_view()),
    path('booklist/<int:id>/', views.SecondBookListView.as_view()),
    path('<int:id>/', views.SecondBookView.as_view()),
    path('categoryBook/<int:id>/', views.CategoryBookView.as_view()),
    path('search/', views.BookSearchView.as_view()),
    path('search_by_name/', views.SearchBooksByNameView.as_view()),
    # 根据关键字搜索分类
    path('search_category/', views.SearchCategoryView.as_view()),
    # 操作原图书信息
    path('origin/', views.OriginBookInfoView.as_view()),
    # 操作二手书信息
    path('second/', views.SecondBookInfoView.as_view()),
    # 根据用户ID获取所售的所有商品
    path('idall/', views.AllByIdView.as_view()),
]
