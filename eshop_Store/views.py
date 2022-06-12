from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
# Create your views here.
from eshop_Cart.models import CartItem
from eshop_Cart.views import _cart_id
from eshop_Home.models import Category
from eshop_Store.models import Product


#THIS FUNCTION FOR GET ALL PRODUCT FORM CATEGORIES
#----------------------------------------------
def store(request,category_slug=None):
    if category_slug is not None:
        categories= get_object_or_404(Category,slug=category_slug)
        products =Product.objects.filter(category=categories , is_available=True).order_by('id')
        paginator =Paginator(products,6)
        page =request.GET.get('page')
        page_products =paginator.get_page(page)
        products_count=products.count()
    else:
        products= Product.objects.filter(is_available=True)
        paginator =Paginator(products,6)
        page =request.GET.get('page')
        page_products= paginator.get_page(page)
        products_count=Product.objects.count()


    context={
        'products':page_products,
        'products_count':products_count
    }
    return render(request,'shared/eshop_store/store.html',context)


#THIS FUNCTION FOR GET PRODUCT ON THE SINGLE PAGE....
#----------------------------------------------------
def product_detail(request,category_slug,product_slug):
    try:
        single_product= Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    context ={
        'single_product':single_product,
        'in_cart':in_cart,

    }
    return render(request,'shared/eshop_store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword= request.GET['keyword']
        if keyword:
            products =Product.objects.order_by('created_data').filter(Q(description__icontains=keyword) |Q(product_name__icontains=keyword))
            products_count =products.count()
            context ={
                'products':products,
                'products_count':products_count
            }
            return render(request,'shared/eshop_store/store.html',context)