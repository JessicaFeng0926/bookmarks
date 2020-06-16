from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    '''用户活动模型类'''
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    # 下面三个字段必须搭配起来使用，这样才能创建一个特殊的外键
    # 这主要是因为每个模型只能有一个普通的外键，而用户活动中的user字段已经是外键了
    # 所以想要再指向Image模型的话就只能创建特殊外键了
    # 这个字段允许我们从目前项目里的所有模型类中选择要使用的类
    # 如果加上参数limit_choices_to，就会限制在一个范围内选择
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    # 这是要指向的模型的主键
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    # 这个字段不会在数据库中创建，它只是负责管理上面两个字段
    target = GenericForeignKey('target_ct','target_id')

    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)