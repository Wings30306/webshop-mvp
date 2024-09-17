from django.forms import ModelForm
from .models import Order, OrderLineItem

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "delivery_address_line1", "delivery_address_postcode", "delivery_address_town", "delivery_address_country"]