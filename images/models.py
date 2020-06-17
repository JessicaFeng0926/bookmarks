from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Image(models.Model):
    # 一对多关系
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name = 'images_created',
                             on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    # 多对多关系
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name = 'images_liked',
                                        blank = True)
    # 统计点赞数
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('images:detail',args=[self.id,self.slug])

