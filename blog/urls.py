from django.urls import path
from .views import *

app_name = "blog"
urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    path('news-list/',NewsListView.as_view(),name="news-list"),
    path('search/',SearchResultsView.as_view(), name='search'),
    path('add-news/',NewsCreateView.as_view(), name='add-news'),
    path('edit-news/<int:pk>/',NewsUpdateView.as_view(), name='edit-news'),
    path('delete-news/<int:pk>/',NewsDeleteView.as_view(), name='delete-news'),
    path('news-list/<slug:category>/',NewsListView.as_view(),name="news-list-category"),
    path('news/<int:year>/<int:month>/<int:day>/<str:slug>/',NewsDetailView.as_view() , name='news_detail'),

]