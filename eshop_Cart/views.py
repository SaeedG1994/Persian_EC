from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from eshop_Cart.models import Cart, CartItem
from eshop_Store.models import Product, Variation


#THIS FUNCTION FOR GET SESSION COOKIES  | OR CREATE A SESSION COOKIES
#--------------------------------------------------------------------
def _cart_id(request):
    cart =request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



#THIS FUNCTION FOR ADD PRODUCT ON THE CART / ADD ITEM WHIT OUT THE LOGIN ON THE PANEL
#--------------------------------------------------------------------
def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    #IF THE USER IS AUTHENTICATED
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # INCREACE  THE CART  ITEM QUANTITY...
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # CREATE A ITEM.....
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # IF THE USER  NOT  IS AUTHENTICATED
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart =Cart.objects.get(cart_id=_cart_id(request)) # GET THE CART USING THE CART_ID PRESENT IN THE SESSION
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        is_cart_item_exist = CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exist:
            cart_item =CartItem.objects.filter(product=product,cart=cart)

            # EXISTING_VARIATION --> DATABASE
            # CURRENT VARIATION --> PRODUCT_VARIATION
            # ITEM_ID -- > DATABASE

            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                #INCREACE  THE CART  ITEM QUANTITY...
                index = ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
            else:
                # CREATE A ITEM.....
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity= 1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



#THIS IS THE FUNCTION CART
#--------------------------------------------------------------------
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart =Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax =(2 * quantity)/100
        grand_total= total + tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,

    }
    return render(request,'shared/eshop_store/cart.html',context)


#THIS FUNCTION FOR REMOVE THE ITEM  WHIT MINUS ADN PLUS  -  1  +  IN CART PAGE
#--------------------------------------------------------------------
def remove_cart(request,product_id,cart_item_id):

    product= get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item =CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


#THIS  FUNCTION FOR  REMOVE ITEM FROM THE  ( CART )
#--------------------------------------------------------------------
def remove_cart_item(request,product_id,cart_item_id):

    product =get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_item =CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


#THIS FUNCTION FOR CHECK USER BEFORE ORDER PLACE
#-----------------------------------------------
@login_required(login_url='login_user')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * quantity) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }
    return render(request,'shared/eshop_store/checkout.html',context)