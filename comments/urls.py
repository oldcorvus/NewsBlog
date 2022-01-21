from django.urls import path
from .views import *

app_name = "comment"
urlpatterns = [

    path('news/<int:id>',CommentCreateView.as_view() , name='add-comment'),
    path('news/<int:id>/<int:reply>',CommentCreateView.as_view() , name='add-reply'),
    path('news/approve/<int:id>',ApproveComment.as_view() , name='approve-comment'),

]