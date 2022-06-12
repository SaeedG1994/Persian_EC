from django.contrib import admin
from .models import Payment,Order,OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','is_ordered','status','order_number']


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','user','product','ordered']


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)