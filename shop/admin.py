from django.contrib import admin
from .models import ShopItem

# Register your models here.
admin.site.register(ShopItem)

class ShopItemAdmin():
    """
    Lists fields for display in admin, fields for search,
    fields to prepopulate
    """

    list_display = ('title', 'slug', 'price')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}