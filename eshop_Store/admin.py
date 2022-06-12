from django.contrib import admin

# Register your models here.
from eshop_Store.models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','stock','price','category','is_available','created_data')
    prepopulated_fields = {'slug':('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)