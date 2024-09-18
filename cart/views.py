from django.shortcuts import render, reverse
from .contexts import cart_contents
import stripe
import os
if os.path.isfile("env.py"):
    import env
from webshop_mvp import settings
from .models import Order, OrderLineItem
from shop.models import ShopItem
# from .forms import OrderForm

stripe.api_key = os.getenv("STRIPE_SECRET")

# Create your views here.
from django.shortcuts import render, redirect

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """

    

    context = {
        "form": OrderForm()
    }

    return render(request, 'cart/cart.html', context)

def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    
    cart = request.session.get('cart', {})

    
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(view_cart)

def create_checkout_session(request):
    """ Create the order in the database and send checkout session object to Stripe """
    ## Code for form validation/saving

    ## Send relevant data to Stripe
    

def checkout_success(request, order_id):
    """ Display the order confirmation page when payment is successful """

    order = Order.objects.get(id=order_id)
    # When checkout session is successful, set payment status to True
    order.order_paid = True
    order.save()

    request.session["cart"] = {} # Cart is cleared

    # Display order confirmation page
    context = {
        "order": order,
        "order_total": "TBC",
    }

    return render(request, 'cart/order_confirmation.html', context) 