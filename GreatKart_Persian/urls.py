"""GreatKart_Persian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from azbankgateways.urls import az_bank_gateways_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from eshop_Home import views

from azbankgateways.urls import az_bank_gateways_urls

from eshop_Orders.views import go_to_gateway_view, callback_gateway_view

urlpatterns = [
    path('', include('eshop_Home.urls')),
    path('', include('eshop_Accounts.urls')),
    path('newAdmin/', admin.site.urls),

    path('store/', include('eshop_Store.urls')),
    path('carts/', include('eshop_Cart.urls')),
    path('orders/',include('eshop_Orders.urls')),

    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-gatewey/',go_to_gateway_view,name='go-to-gatewey'),

    path('callback-gateway/',callback_gateway_view),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
