import time

from azbankgateways.models import Bank, PaymentStatus
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
import datetime

from zeep import Client, client

from eshop_Cart.models import CartItem
from eshop_Orders.form import OrderForm
from eshop_Orders.models import Order, OrderProduct, Payment
from eshop_Store.models import Product

import requests
import json

import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    # grand_total = 0
    # tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # Like this : 2021 03 05
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'shared/eshop_Orders/payments.html', context)
    else:
        return redirect('checkout')


def go_to_gateway_view(request,total=0, quantity=0):
    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (0 * total) / 100
    grand_total = total + tax
    form = OrderForm(request.POST)

    data = Order()
    data.order_total = grand_total
    data.tax = tax


    order = Order.objects.filter(user=request.user,is_ordered=False).first()
    if Bank.status == PaymentStatus.choices:
        order.is_ordered = True
        order.save()
        print('True')
    elif Bank.status == PaymentStatus.choices:
        order.is_ordered = False
        order.save()
        print('False')

    #  # Mover the CartItems ot Order Product Table
    # cart_items = CartItem.objects.filter(user=request.user)
    # for item in cart_items:
    #     orderProduct = OrderProduct()
    #     orderProduct.order_id = order.id
    #     # orderProduct.payment = payment
    #     orderProduct.user_id = request.user.id
    #     orderProduct.product = item.product_id
    #     orderProduct.quantity = item.quantity
    #     orderProduct.product_price = item.product.price
    #     orderProduct.ordered = True
    #     orderProduct.save()
    #
    # # Reduce the quantity of the sold products
    # product = Product.objects.get(id=item.product_id)
    # product.stock -= item.quantity
    # product.save()

    # Clear  Cart
    CartItem.objects.get(user=request.user).delete()


    # خواندن مبلغ از هر جایی که مد نظر است
    amount = data.order_total

    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '09159150915'  # اختیاری

    factory = bankfactories.BankFactory()

    bank = factory.create()  # or factory.create(bank_models.BankType.BMI) or set identifier
    bank.set_request(request)
    bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    bank.set_client_callback_url('/callback-gateway/')
    bank.set_mobile_number(user_mobile_number)  # اختیاری

    # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
    # پرداخت برقرار کنید.
    bank_record = bank.ready()

    # هدایت کاربر به درگاه بانک
    return bank.redirect_gateway()


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return render(request,'shared/eshop_Orders/success_Payments.html')

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return render(request,'shared/eshop_Orders/Unsuccessful_payment.html')
