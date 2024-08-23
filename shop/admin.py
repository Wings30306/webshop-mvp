from django.contrib import admin
from .models import ShopItem

# Register your models here.
admin.site.register(ShopItem)

class ShopItemAdmin():
    """
    Lists fields for display in admin, fields for search,
    fields to prepopulate
    """

    list_display = ('item_name', 'price')
    search_fields = ['item_name', 'description']
    prepopulated_fields = {'slug': ('item_name',)}