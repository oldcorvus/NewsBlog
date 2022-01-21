from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name='user_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply_comment')
    is_reply = models.BooleanField(default=False)
    body = RichTextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    news_comment = models.ForeignKey('blog.News',blank=True,null=True, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f'{self.author} - {self.body[:30]}'

    class Meta:
        ordering = ('-created',)
        