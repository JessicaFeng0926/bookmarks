from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from .forms import LoginForm,UserRegistrationForm,UserEditForm,\
    ProfileEditForm
from .models import Profile,Contact
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
# Create your views here.

def user_login(request):
    '''登录视图'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 用于验证用户名和密码是否正确
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                # 检查账号是否已被激活
                if user.is_active:
                    # 把用户设置到当前会话中
                    login(request,user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})

@login_required
def dashboard(request):
    # 取出所有的用户活动
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    
    if following_ids:
        # 如果这个用户关注了别人，那就只显示他关注的人的活动
        actions = actions.filter(user_id__in=following_ids)
    # 只显示前十条信息就可以了
    # 这里用的select_related方法把一对多关系的表里的数据也一起取出来
    # 这样后面用的时候就不需要重复访问了
    # 因为select_related不能处理GenericForeignKey的关系
    # 所以这里又添加了prefetch_related来处理这种特殊的关系
    actions = actions.select_related('user','user__profile').\
        prefetch_related('target')[:10]
    return render(request,
                  'account/dashboard.html',
                  {'section':'dashboard',
                   'actions':actions})

def register(request):
    '''注册视图'''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            # 创建一个新的简历对象并绑定一对一关系，保存到数据库
            Profile.objects.create(user=new_user)
            # 添加用户活动
            create_action(request.user,'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form':user_form})

@login_required
def edit(request):
    '''修改个人信息'''
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated '\
                             'successfully')
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form':user_form,
                  'profile_form':profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section':'people',
                  'users':users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section':'people',
                  'user':user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from = request.user,
                    user_to = user
                )
                # 添加用户活动
                create_action(request.user,'is following',user)
            else:
                Contact.objects.filter(
                    user_from = request.user,
                    user_to = user
                ).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
        



