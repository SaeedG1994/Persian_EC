from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    category_name= models.CharField(max_length=55,unique=True,verbose_name='دسته بندی کلی ')
    slug= models.SlugField(max_length=100,unique=True, verbose_name=' آدرس اسلاگ ')
    description= models.TextField(max_length=255,blank=True, verbose_name='توضیحات ')
    cat_image= models.ImageField(upload_to='photos/category',blank=True,verbose_name='عکس دسته بندی ')

    class Meta:
        verbose_name= 'دسته بندی'
        verbose_name_plural ='دسته بندی کلی'


    def __str__(self):
        return self.category_name

    #FOR GET SLUG URL CATEGORIES
    #__________________________
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])


