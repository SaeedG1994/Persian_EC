from django.urls import path
from eshop_Home import views

urlpatterns = [
    path('',views.index, name='index')
]