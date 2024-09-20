from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse
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
        "stripe_publ_key": os.getenv("STRIPE_PUBLISHABLE")
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
    ## Send relevant data to Stripe
    try:
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            line_items=cart_contents(request)["stripe_line_items"],
            mode='payment',
            billing_address_collection='auto',
            shipping_address_collection={
                'allowed_countries': [ # complete list of country codes allowed by Stripe
                    'AC', 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AT',
                    'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI',
                    'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY',
                    'BZ', 'CA', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO',
                    'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC',
                    'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FO', 'FR', 'GA',
                    'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ',
                    'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID',
                    'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP',
                    'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB',
                    'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD',
                    'ME', 'MF', 'MG', 'MK', 'ML', 'MM', 'MN', 'MO', 'MQ', 'MR', 'MS', 'MT',
                    'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NG', 'NI', 'NL',
                    'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK',
                    'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU',
                    'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM',
                    'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SZ', 'TA', 'TC', 'TD', 'TF',
                    'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW',
                    'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VN', 'VU',
                    'WF', 'WS', 'XK', 'YE', 'YT', 'ZA', 'ZM', 'ZW', 'ZZ'
                ]},
            return_url=os.getenv("ROOT_URL") + '/cart/return/{CHECKOUT_SESSION_ID}',
        )
        return JsonResponse({'clientSecret': session.client_secret})
    except Exception as e:
        # Log the exception if necessary
        print(f"Error creating checkout session: {e}")
        
        # Return a 500 error with an empty HttpResponse
        return HttpResponse(status=500)

    

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


def session_status(request, SESSION_ID):
    """ This function needs to run in order to correctly set the details on the return view """
    session = stripe.checkout.Session.retrieve(SESSION_ID)

    return JsonResponse({"status": session.status, "customer_email": session.customer_details.email})


def return_view(request, CHECKOUT_SESSION_ID):
    context = {
        "session_id": CHECKOUT_SESSION_ID
    }
    
    stripe_session_data = stripe.checkout.Session.retrieve(CHECKOUT_SESSION_ID)
    shipping = stripe_session_data.shipping_details
    is_paid = stripe_session_data.payment_status == "paid"

    # Create order
    order = Order.objects.create(
        customer_name=shipping.name,
        shipping_line1=shipping.address.line1,
        shipping_line2=shipping.address.line2,
        shipping_town_or_city=shipping.address.city,
        shipping_postal_code=shipping.address.postal_code,
        shipping_county_or_state=shipping.address.state,
        shipping_country=shipping.address.country,
        order_paid=is_paid
    )

    # Create order line items
    cart = request.session.get('cart', {})
    for item_id in cart.keys():
        item = ShopItem.objects.get(id=item_id)
        quantity = cart[item_id]
        order = Order.objects.get(id=order.id)
        OrderLineItem.objects.create(item=item, order=order, quantity=quantity)

    # Empty cart: 
    request.session["cart"] = {} # Cart is cleared


    return redirect(reverse("checkout_success", args=[order.id]))