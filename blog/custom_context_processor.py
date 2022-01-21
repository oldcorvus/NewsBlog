from .models import Category, News
from django.core.paginator import Paginator

def poular_news_renderer(request):
    
    paginator = Paginator(News.objects.published().order_by('-views'), 1)

    page_number = request.GET.get('page_view')
    page_obj = paginator.get_page(page_number)
    return {
       'popular_news': page_obj,
    }
def poular_news_date_renderer(request):
    
    paginator = Paginator(News.objects.published().order_by('-publish'), 2)

    page_number = request.GET.get('page_popular')
    page_obj = paginator.get_page(page_number)
    return {
       'page_popular_obj': page_obj,
    }

def categories_renderer(request):
    return {
       'categories': Category.objects.filter(status = True),
    }