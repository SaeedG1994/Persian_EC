from django.db import models

# Create your models here.
from eshop_Accounts.models import Account
from eshop_Store.models import Product, Variation

# THE PAYMENT CLASS
#------------------
class Payment(models.Model):
    user =models.ForeignKey(Account,on_delete=models.CASCADE,verbose_name='یوز پرداخت کننده ')
    payment_id =models.CharField(max_length=100,verbose_name='آیدی پرداخت ')
    payment_method= models.CharField(max_length=100,verbose_name='روش پرداخت ')
    amount_paid =models.CharField(max_length=100,verbose_name='مبلغ پرداخت شده ')
    status = models.CharField(max_length=100,verbose_name='وضعیت پرداخت ')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد ')


    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural ='بخش پرداخت ها '

# THE ORDER CLASS
#------------------
class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,verbose_name='یوز سفارش دهنده ')
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='نوع پرداخت ')
    order_number =models.CharField(max_length=20,verbose_name='شماره ی سفارش ')
    first_name =models.CharField(max_length=50,verbose_name='نام ')
    last_name =models.CharField(max_length=50,verbose_name='نام خانوادگی ')
    phone =models.CharField(max_length=15,verbose_name='همراه ')
    email =models.EmailField(max_length=50,verbose_name='ایمیل ')
    address_line_1 =models.CharField(max_length=50,verbose_name='آدرس اول ')
    address_line_2 =models.CharField(max_length=50,blank=True,verbose_name='آدرس دوم ')
    country =models.CharField(max_length=50,verbose_name='کشور ')
    state =models.CharField(max_length=50,verbose_name='دولت ')
    city =models.CharField(max_length=50,verbose_name=' شهر ')
    order_note =models.CharField(max_length=100,blank=True,verbose_name='یادداشت سفارش ')
    order_total = models.FloatField(verbose_name='جمع سفارش')
    tax = models.FloatField(verbose_name='مالیات ')
    status =models.CharField(max_length=10, choices=STATUS,default='New',verbose_name='وضعیت محصول ')
    ip =models.CharField(blank=True,max_length=20,verbose_name='آی پی کاربر ')
    is_ordered= models.BooleanField(default=False,verbose_name='سفارش داده شده است  ')
    created_at =models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد ')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='تاریخ آپدیت ')


    def __str__(self):
        return self.first_name



    #GET THE FIRST NAME AND LAST NAME
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    #GET THE ADDRESS 1 + ADDRESS 2
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural ='بخش سفارش ها  '

# THE ORDER PRODUCT CLASS
#________________________
class   OrderProduct(models.Model):
    order   = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سفارش ')
    payment =models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True,verbose_name='نوع پرداخت ')
    user =models.ForeignKey(Account,on_delete=models.CASCADE,verbose_name='یوز سفارش دهنده ')
    product =models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول سفارش داده ')
    variation =models.ForeignKey(Variation,on_delete=models.CASCADE,verbose_name='تنوع محصول ')
    color =models.CharField(max_length=50,verbose_name='رنگ محصول ')
    size =models.CharField(max_length=50,verbose_name='سایز محصول ')
    quantity =models.IntegerField(verbose_name='تعداد محصول ')
    product_price =models.IntegerField(verbose_name='قیمت محصول ')
    ordered =models.BooleanField(default=False,verbose_name='سفارش داده شده ')
    created_at =models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد ')
    updated_at =models.DateTimeField(auto_now=True,verbose_name='تاریخ آپدیت ')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'بخش سفارش محصولات '