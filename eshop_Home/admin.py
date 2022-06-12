from django.contrib import admin

# Register your models here.
from eshop_Home.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','slug','description']
    prepopulated_fields = {'slug':('category_name',)}




admin.site.register(Category,CategoryAdmin)