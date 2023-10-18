# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.contrib import messages
# Internal:
from products.models import Album
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def bag_view(request):
    """
    A function to show bag page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    A function to add a quantity of the specified product to the shopping bag
    """
    album = get_object_or_404(Album, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    while True:
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity < 1:
                quantity = 1
                messages.warning(request, "You can't choose less than 1")
            if quantity > 5:
                quantity = 5
                messages.warning(request, "Sorry, \
                    You can't choose more than 5")
            break
        except ValueError:
            messages.warning(request, "Invalid input")
            return redirect(redirect_url)
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Added {album.name} to your bag')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {album.name} to your bag')
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    A function to adjust the quantity of the
    specified product to the specified amount
    """
    album = get_object_or_404(Album, pk=item_id)

    while True:
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity < 1:
                quantity = 1
                messages.warning(request, "You can't choose less than 1")
            if quantity > 5:
                quantity = 5
                messages.warning(request, "Sorry, \
                    You can't choose more than 5")
            break
        except ValueError:
            messages.warning(request, "Invalid input")
            return redirect(reverse('bag'))

    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})
    bag[item_id] = quantity
    messages.success(request, f'Updated {album.name} quantity')
    request.session['bag'] = bag
    return redirect(reverse('bag'))


def remove_from_bag(request, item_id):
    """
    A function to remove the item from the shopping bag
    """
    try:
        album = get_object_or_404(Album, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {album.name} from your bag')
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item {e}')
        return HttpResponse(status=500)
