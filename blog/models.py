
from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

from comments.models import Comment

# Create your models here.

class NewsManagers(models.Manager):
    def published(self):
        return self.filter(status="P")


class CategoryManagers(models.Manager):
    def active(self):
        return self.filter(status=True)


class News(models.Model):
    STATUS_CHOICES = (
        ('P', 'Published'),
        ('D', 'Draft'),
    )
    title = models.CharField(max_length=128, null=False, blank=False, verbose_name="عنوان")
    content = RichTextUploadingField(verbose_name="متن")
    cover = models.ImageField(upload_to='images/article/%Y/%m/%d/')
    promote =  models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, default="", verbose_name="لينك")
    created =jmodels.jDateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="تاريخ ساخت")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاريخ تغيير")
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاريخ انتشار")
    category = models.ForeignKey('Category',on_delete=models.CASCADE, verbose_name="دسته بندي", related_name="news")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نويسنده",related_name="news")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d", verbose_name="وضعيت")
    objects = NewsManagers()
    views = models.PositiveIntegerField(default= 0)
    
    def get_absolute_url(self):
         return reverse('blog:news_detail', args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

    def active_categories(self):
        return self.category.filter(status=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-publish',)
    


  
class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False, verbose_name="عنوان")
    cover = models.ImageField(upload_to='images/category/%Y/%m/%d/')
    slug = models.SlugField(max_length=100, unique=True, default="", verbose_name="لينك")
    status = models.BooleanField(default=True, verbose_name="نمايش داده شود ؟")
    description = models.CharField(max_length=512, null=False, blank=False, default="", verbose_name="توضيحات")
    parent = models.ForeignKey('self', default=None, blank=True, null=True, related_name="children",
    on_delete=models.SET_NULL, verbose_name="زیر دسته")
    objects = CategoryManagers()

    def get_absolute_url(self):
         return reverse('blog:news-list-category', args=[self.slug])

    class Meta:
        verbose_name = 'دسته بندي'
        verbose_name_plural = 'دسته بندي ها'
        ordering = ['parent__id']

    def __str__(self):
        return self.title