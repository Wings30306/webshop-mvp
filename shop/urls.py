from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopItemList.as_view(), name='home'),
    path('<slug:slug>/', views.item_detail, name="item_detail"),
]