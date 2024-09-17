from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path("checkout-session", views.create_checkout_session, name="create_checkout_session"),
    path("checkout-success/<order_id>", views.checkout_success, name="checkout_success"),
    
]