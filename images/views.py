from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger
import redis
from django.conf import settings

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action
# Create your views here.

# 连接redis数据库
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                username=settings.REDIS_USERNAME,
                password=settings.REDIS_PASSWORD)

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            # 添加用户活动
            create_action(request.user,'bookmarked image',new_item)
            messages.success(request,'Image added successfully')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section':'images',
                  'form':form}) 


def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    # 图片访问数量加1
    # 参数是key，key不存在就新建，存在就把值加1
    total_views = r.incr(f'image:{image.id}:views')
    # 图片排序，使用redis的有序集合，
    # 每访问一次，权重score就加1
    # 这个集合的键是image_ranking
    r.zincrby('image_ranking',1,image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section':'images',
                  'image':image,
                  'total_views':total_views})

@ajax_required
@login_required
@require_POST
def image_like(request):
    '''用户点赞'''
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # 添加用户活动
                create_action(request.user,'likes',image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    '''列出所有图片'''
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        # 如果是ajax请求，那就是滑到底了，什么也不用返回
        if request.is_ajax():
            return HttpResponse('')
        # 如果不是ajax请求，那就返回最后一页
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section':'images','images':images})
    return render(request,
                  'images/image/list.html',
                  {'section':'images','images':images})


@login_required
def image_ranking(request):
    '''按照图片访问量来显示图片'''
    image_ranking = r.zrange('image_ranking',0,-1,desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # 获取对应的图片对象
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # 因为从数据库里查出来之后顺序就还是按照默认的id大小排列了，
    # 下面就是要恢复访问量的降序排列
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section':'images',
                  'most_viewed':most_viewed})
    
