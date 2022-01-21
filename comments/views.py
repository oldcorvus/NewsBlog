from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.views import View 

from comments.forms import CommentFrom
from .models import Comment
from blog.models import News
# Create your views here.
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentFrom
    
    def form_valid(self, form):
        global news_obj
        news_obj = get_object_or_404(News, pk=self.kwargs['id'])
        form.instance.author = self.request.user
        form.instance.news_comment = news_obj
        if self.kwargs.get('reply'):
            form.instance.is_reply = True
            form.instance.reply = get_object_or_404(Comment, pk=self.kwargs['reply'])

        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
         global news_obj
         return reverse('blog:news_detail', args=[news_obj.publish.year,news_obj.publish.month,news_obj.publish.day,news_obj.slug])

class ApproveComment(LoginRequiredMixin, View):
    def get(self, request ,id):
        comment = get_object_or_404(Comment,id =id)
        comment.approve = True
        comment.save()
        return redirect(to='blog:index')
