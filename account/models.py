from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    '''用户额外的个人信息'''
    # 和django自带的用户模型类形成了一对一的关系
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'