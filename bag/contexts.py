# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
# Internal:
from products.models import Album
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def bag_contents(request):
    """
    A function to collect all bag data and send it on all website pages
    """
    bag_items = []
    bag = request.session.get('bag', {})
    total = 0
    product_count = 0

    for item_id, quantity in bag.items():
        album = get_object_or_404(Album, pk=item_id)
        total += quantity * album.price
        product_count += quantity
        subtotal = quantity * album.price
        bag_items.append({
            'album': album,
            'item_id': item_id,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
