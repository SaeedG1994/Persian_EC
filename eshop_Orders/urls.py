from django.urls import path
from eshop_Orders import views



urlpatterns = [
        path('place_order/',views.place_order,name='place_order'),






]