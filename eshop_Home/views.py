from django.shortcuts import render
from eshop_Store.models import Product



def index(request):
    products=Product.objects.filter(is_available=True)
    context={
        'products':products
    }
    return render(request,'shared/index.html',context)

