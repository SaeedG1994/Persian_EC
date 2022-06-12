from django.db import models

# Create your models here.
from eshop_Accounts.models import Account
from eshop_Store.models import Product, Variation


#THIS IS CART MODEL
#------------------
class Cart(models.Model):
    cart_id     =models.CharField(max_length=255,blank=True,verbose_name='آیدی سبد خرید ')
    data_added  =models.DateField(auto_now_add=True,verbose_name='تاریخ افزودن ')

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'سبد'
        verbose_name_plural = 'سبد خرید'

#THIS IS CART ITEM   |   THIS CLASS HAS TWO RELATION WHIT (PRODUCT MODEL  AND CART MODEL )
#------------------
class CartItem(models.Model):
    user      =models.ForeignKey(Account,on_delete=models.CASCADE ,null=True)
    product   =models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول ')
    variations =models.ManyToManyField(Variation,blank=True,verbose_name='تنوع محصول با کدام آیتم')
    cart      =models.ForeignKey(Cart,on_delete=models.CASCADE,verbose_name='سبد خرید ',null=True)
    quantity  =models.IntegerField(verbose_name='تعداد ')
    is_active =models.BooleanField(default=True,verbose_name='فعال/غیرفعال ')


    class Meta:
        verbose_name = 'محصول به سبد خرید '
        verbose_name_plural = 'محصولات سبد خرید'

    def __unicode__(self):
        return self.product

    #THIS FUNCTION FOR MULTIPLE  ( PRODUCT )
    #--------------------------------------
    def sub_total(self):
        return self.product.price * self.quantity

