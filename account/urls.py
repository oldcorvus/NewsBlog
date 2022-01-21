from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "account"
urlpatterns = [
    path('login/',UserLogin.as_view(),name="login"),
    path('logout/',UserLogout.as_view(),name="logout"),
    path('register/',UserRegister.as_view(),name="register"),
    path('profile/<slug:user>/',UserDetailView.as_view(),name="profile"),
    path('user-news-list/<int:user>/', UserNewsListView.as_view(), name="user-news"),
    path('profile/<str:username>/edit/',profile_edit,name="profile_edit"),
]