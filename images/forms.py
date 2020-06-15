from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model =  Image
        fields = ['title','url','description']
        widgets = {
            # 对用户不可见
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        # 只允许上传jpg格式的图像
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not \
                match valid image extensions.')
        return url
    
    def save(self,
            force_insert=False,
            force_update=False,
            commit=True):
        '''覆盖了原来的save方法'''
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extension}'
        
        # 下载图片
        response = request.urlopen(image_url)
        # 后面的这个image是数据库里的image字段
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image
