from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import ShopItem

def cart_contents(request):

    cart_items = []
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
            'item': item,
        })
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
    }

    return context