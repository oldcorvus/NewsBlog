
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from comments.forms import CommentFrom
from .forms import FilterForm
from .models import News
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from ckeditor.widgets import CKEditorWidget
from django.contrib import messages
from django.urls import reverse_lazy

class IndexView(ListView):
    model = News
    paginate_by = 3 
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slidebar'] = News.objects.filter(promote=True,status="P")[:3]
        print(context['slidebar'])
        return context
    def get_queryset(self):
        queryset = News.objects.published()
        return queryset

class SearchResultsView(ListView):
    model = News
    template_name = 'blog/search.html'
    paginate_by = 1

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query,status="P")
        )
        return object_list

    
class NewsListView(ListView):
    model = News
    paginate_by = 2
    form_class = FilterForm 
    template_name = 'blog/news-list-page.html'
    
    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        paginator = Paginator(News.objects.annotate(num=Count('comments')).order_by('-num'), 1)
        page_number = self.request.GET.get('page_comments')
        page_obj = paginator.get_page(page_number)
        context['news_popular_comments'] = page_obj
        return context
    

    def get_queryset(self):
        queryset = News.objects.published()

        if self.kwargs.get('user'):
            queryset= queryset.filter(author =self.kwargs.get('user'))
        if self.kwargs.get('category'):
            queryset= queryset.filter(category__slug =self.kwargs.get('category'))
        if self.request.GET.get('start_date') and self.request.GET.get('finish_date'):
            start = self.request.GET.get('start_date')
            finish = self.request.GET.get('finish_date')
            queryset = News.objects.filter(publish__gte= start, publish__lt = finish)
        if self.request.GET.get('filter') == "تعداد بازدید(زیاد به کم)":
            queryset = queryset.order_by('-views')
        elif self.request.GET.get('filter') == "تعداد بازدید(کم به زیاد)":
                queryset = queryset.order_by('views')
        elif self.request.GET.get('filter') == "تاریخ (جدید به قدیمی)":
                queryset = queryset.order_by('-publish')
        elif self.request.GET.get('filter') == "تاریخ (قدیمی به جدید)":
                queryset = queryset.order_by('publish')
        return queryset
    
class NewsDetailView(DetailView):
    
    model = News
    template_name = 'blog/news-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_reply=False, approve=True)
        if self.request.user == self.object.author:
            context['unapproved_comments'] =self.object.comments.filter(approve=False)
        context['form'] = CommentFrom()
        return context
    
    def get_object(self) :
        news = get_object_or_404(News,slug=self.kwargs.get('slug'))
        news.views = F('views') + 1
        news.save(update_fields=['views'])
        news.refresh_from_db()
        return news
    
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = "blog/edite-page.html"
    fields = ['title','content','cover','category','status']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = CKEditorWidget()
        return form
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'][:30],allow_unicode=True)
        messages.success(self.request, "خبر شما با موفقيت منشتر شد")
        return super(NewsCreateView, self).form_valid(form)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = "blog/edite-page.html"
    fields = ['title','content','cover','category','status']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ويرايش خبر"
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = CKEditorWidget()
        return form
    def test_func(self):
       news = self.get_object()
       if self.request.user == news.author:
            return True
       return False
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'][:30],allow_unicode=True)
        messages.success(self.request, "خبر شما با موفقيت ويرايش يافت")

        return super(NewsUpdateView, self).form_valid(form)
    
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('blog:index')
    def get(self, request, *args, **kwargs):
            messages.success(self.request, "خبر شما با موفقيت حذف يافت")
            return self.post(request, *args, **kwargs)

