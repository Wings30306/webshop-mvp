from django.shortcuts import render, reverse
from .contexts import cart_contents
import stripe
import os
if os.path.isfile("env.py"):
    import env

from .models import Order, OrderLineItem
from shop.models import ShopItem
from .forms import OrderForm

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

    # Create checkout session
    try:
        # Create the order with line items and address
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()

            cart = request.session.get('cart', {})
            print(cart)
            for item_id in cart.keys():
                item = ShopItem.objects.get(id=item_id)
                quantity = cart[item_id]
                order = Order.objects.get(id=order.id)
                OrderLineItem.objects.create(item=item, order=order, quantity=quantity)

        checkout_session = stripe.checkout.Session.create(
            line_items=cart_contents(request)['stripe_line_items'],
            mode='payment',
            success_url="https://8000-wings30306-webshopmvp-7zs4od7kd3m.ws.codeinstitute-ide.net/cart/checkout-success/" + str(order.id),
            cancel_url="https://8000-wings30306-webshopmvp-7zs4od7kd3m.ws.codeinstitute-ide.net/cart"
        )
        print(checkout_session)
        
    except Exception as e:
        print(e)
        return str(e)

    return redirect(checkout_session.url, code=303)

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