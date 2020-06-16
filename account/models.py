from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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


class Contact(models.Model):
    '''这是反映用户之间关系的中间表'''
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# 给用户模型动态添加多对多关系
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                        through=Contact,
                        # “我”是粉丝
                        related_name='followers',
                        # 取消对称，这意味着我粉了你，不代表你也粉了我
                        symmetrical=False))