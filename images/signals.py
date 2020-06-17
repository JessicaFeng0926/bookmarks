from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


# 这是一个接收器函数
# 把它绑定到m2m_changed信号上
# 每次一张图片的点赞数发生变化，它就能接收到
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()