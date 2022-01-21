from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="كاربر" , related_name='profile')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name="توضيحات")
    avatar = models.ImageField(upload_to='images/users/%Y/%m/%d/')

    class Meta:
        verbose_name = 'پروفايل كاربر'
        verbose_name_plural = 'پروفايل كاربرها'

    def __str__(self):
        return self.user.username
    
def save_profile(sender, **kwargs):
        if kwargs['created']:
            p = UserProfile(user=kwargs['instance'])
            p.save()

post_save.connect(save_profile, sender=User)