from django.db import models
from shop.models import ShopItem

# Create your models here.
class Order(models.Model):
    customer_name = models.CharField(max_length=200) # Do not make unique, we want the same customer to be able to order again
    delivery_address_line1 = models.CharField(max_length=200)
    delivery_address_line2 = models.CharField(max_length=200, blank=True, null=True) # Allow to be blank, not all addresses contain this line
    delivery_address_town = models.CharField(max_length=200)
    delivery_address_postcode = models.CharField(max_length=20)
    delivery_address_county = models.CharField(max_length=100, blank=True, null=True) # Allow to be blank, not all countries require this line
    delivery_address_country = models.CharField(max_length=100)
    order_paid = models.BooleanField(default=False) # On creation, the payment has not gone through yet

class OrderLineItem(models.Model):
    item = models.ForeignKey(ShopItem, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name="order_line_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()