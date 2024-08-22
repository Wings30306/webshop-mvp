from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import ShopItem

# Create your views here.


class ShopItemList(generic.ListView):
    """
    Returns all published items in :model:`shop.ShopItem`
    and displays them in a page of six items. 
    **Context**

    ``queryset``
        All published instances of :model:`shop.ShopItem`
    ``paginate_by``
        Number of items per page.
        
    **Template:**

    :template:`shop/index.html`
    """
    queryset = ShopItem.objects.all()
    template_name = "shop/index.html"
    paginate_by = 6


def item_detail(request, slug):
    """
    Display an individual :model:`shop.ShopItem`.

    **Context**

    ``item``
        An instance of :model:`shop.ShopItem`.

    **Template:**

    :template:`shop/item_detail.html`
    """
    queryset = ShopItem.objects.all()
    item = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "shop/item_detail.html",
        {
            "item": item,
        },
    )