from django.contrib import admin

# Register your models here.
from eshop_Cart.models import CartItem, Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','data_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active','user')
    list_editable = ('is_active',)
    list_filter = ('product','cart','quantity','is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)