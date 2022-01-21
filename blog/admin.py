from django.contrib import admin
from .models import *
    

def article_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='P')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))

article_published.short_description = "انتشار مقالات"

def article_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status='D')
        if rows_updated == 1:
            message_bit = "پیش‌نویس شد."
        else:
            message_bit = "پیش‌نویس شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))

article_draft.short_description = "پیشنویس مقالات"




class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['title', 'author','status','category']
    list_filter = ['status','publish']
    raw_id_fields = ('author',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status','-publish']
    actions =[article_published, article_draft]




admin.site.register(News, ArticleAdmin)


def category_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status= True)
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))

category_published.short_description = "انتشار دسته بندی "

def category_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status= False)
        if rows_updated == 1:
            message_bit = "پیش‌نویس شد."
        else:
            message_bit = "پیش‌نویس شدند."
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))

category_draft.short_description = "پیشنویس دسته بندی"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover','parent','slug','status']
    search_fields = ['title','description']
    list_filter = ['status']
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    actions =[category_published, category_draft]

admin.site.register(Category, CategoryAdmin)