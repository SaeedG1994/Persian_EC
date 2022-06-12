from django.db import models
# Create your models here.
from django.urls import reverse

from eshop_Home.models import Category

#THIS IS THE PRODUCT CLASS
#-------------------------
class Product(models.Model):
    product_name        =models.CharField(max_length=200,unique=True,verbose_name='نام محصول ')
    slug                =models.SlugField(max_length=200,unique=True,verbose_name='آدرس اسلاگ ')
    description         =models.TextField(max_length=500,blank=True,verbose_name='توضیحات محصول ')
    price               =models.IntegerField(verbose_name='قیمت محصول ')
    images              =models.ImageField(upload_to='photos/products',verbose_name='تصویر محصول ')
    stock               =models.IntegerField(verbose_name=' تعداد کالا در انبار ')
    is_available        =models.BooleanField(default=True,verbose_name='موجود بودن کالا')
    category            =models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='دسته بندی محصول ')
    created_data        =models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد ')
    modified_data       =models.DateTimeField(auto_now=True,verbose_name=' تاریخ ویرایش ')


    def __str__(self):
        return self.product_name


    #THIS FUNCTION FOR GET CATEGORY AND PRODUCT URL FROM THE ( SLUG )
    #---------------------------------------------------------------
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug ,self.slug])


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural ='محصولات'


#WE USE THIS CLASS FOR MANAGE (VARIATION (COLOR  AND  SIZE) THIS CLASS HAS A OBJECTS WHIT (VARIATION CLASS) )
#-----------------------------------------------------------------------------------------------------------
class VariationManger(models.Manager):
    def colors(self):
        return super(VariationManger,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManger,self).filter(variation_category='size',is_active=True)



#THIS IS THE VARIATION CLASS HAS A RELATION (FOREIGNKEY WHIT PRODUCT CLASS )
#-------------------------
variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کدام محصول (تنوع) دارد')
    variation_category  =models.CharField(max_length=100,choices=variation_category_choice,verbose_name='دسته بندی (نوع) بر اساس رنگ - سایز')
    variation_value     = models.CharField(max_length=100,verbose_name='نوع تنوع محصول(مثال : color-آبی) ')
    is_active           = models.BooleanField(default=True,verbose_name='فعال/غیر فعال')
    created_data        =models.DateTimeField(auto_now=True,verbose_name='تاریخ ایجاد')

    objects =VariationManger() # RELATED WHIT UP CLASS

    def __str__(self):
        return self.variation_value

    class Meta:
        verbose_name = 'نوع'
        verbose_name_plural ='نوع محصول (براساس : رنگ - سایز ) '
