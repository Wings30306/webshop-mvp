from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import ShopItem

def cart_contents(request):

    cart_items = []
    stripe_line_items = []
    total = 0
    item_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        item = get_object_or_404(ShopItem, pk=item_id)
        total += item_data * item.price
        item_count += item_data
        cart_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'price': item.price,
            'item': item,
        })

        # # Set line item data for Stripe
        # stripe_line_items.append({
        #     'quantity': item_data,
        #     'price_data': {
        #         "currency": "eur",
        #         "unit_amount": item.price * 100,
        #         "product_data": {
        #             "name": item.item_name,
        #         }
        #     }
        # })

    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
        #'stripe_line_items': stripe_line_items,
    }

    return context