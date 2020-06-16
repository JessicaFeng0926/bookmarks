import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    # 检查一下在过去的一分钟内是否有一样的活动
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    # 先用动词和时间筛选一次
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    # 如果提供了模型，还要用模型筛选一次
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    # 确定过去一分钟内没有类似的活动，才创建
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False