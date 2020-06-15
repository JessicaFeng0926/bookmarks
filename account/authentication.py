from django.contrib.auth.models import User

class EmailAuthBackend(object):
    '''
    用邮箱认证
    '''
    # 下面这两个方法是负责验证用户的backend必须有的
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None