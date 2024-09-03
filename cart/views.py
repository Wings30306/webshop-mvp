from django.shortcuts import render
from .contexts import cart_contents
import stripe
import env
import os

stripe.api_key = os.getenv("STRIPE_SECRET")

# Create your views here.
from django.shortcuts import render, redirect

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')

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
    
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=cart_contents(request)['stripe_line_items'],
            mode='payment',
            success_url="https://8000-wings30306-webshopmvp-7zs4od7kd3m.ws.codeinstitute-ide.net/",
            cancel_url="https://8000-wings30306-webshopmvp-7zs4od7kd3m.ws.codeinstitute-ide.net/",
        )
    except Exception as e:
        print(e)
        return str(e)

    return redirect(checkout_session.url, code=303)