from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('info/', views.InfoView.as_view()),
    path('name/', views.NameView.as_view()),
    path('nickname/', views.NicknameView.as_view()),
    path('avatar/', views.AvatarView.as_view()),
    path('check/', views.CheckView.as_view()),
    path("pwd/", views.PasswordView.as_view()),
    path("address/", views.AddressView.as_view()),
    path('phone/', views.PhoneView.as_view()),
]
