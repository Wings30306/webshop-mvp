from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    # path("checkout-success/<order_id>", views.checkout_success, name="checkout_success"),
    path("session-status/<SESSION_ID>", views.session_status, name="get_session_status"),
    path("return/<CHECKOUT_SESSION_ID>", views.return_view, name="stripe_return_view")
    
]