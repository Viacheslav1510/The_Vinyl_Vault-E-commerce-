# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Internal:
from .models import Wishlist
from products.models import Album
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@login_required
def wishlist(request):
    """
    View wishlist for logged in user
    """
    if request.user.is_authenticated:
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
        items_count = wishlist.count()
    context = {
        'wishlist': wishlist,
        'items_count': items_count
    }
    template = 'wishlist/wishlist.html'

    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id, user_id):
    """
    Add product to wishlist
    """
    product = Album.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
                                product=product,
                                user=user
    )
    if created:
        wishlist_item.save()
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')
    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def remove_from_wishlist(request, wishlist_id):
    """
    Remove item from wishlist
    """
    wishlist_item = Wishlist.objects.get(id=wishlist_id)
    wishlist_item.delete()
    messages.success(request, 'Removed from wishlist!!')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'wishlist' in referer:
            return redirect('wishlist')
        else:
            return redirect(referer)
    else:
        return redirect('wishlist')


@login_required
def add_to_wishlist_all_products(request, product_id, user_id):
    """
    Add product to wishlist on all products page
    """
    product = Album.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
                                product=product,
                                user=user
    )
    if created:
        wishlist_item.save()
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_wishlist_all(request, product_id, user_id):
    """
    Remove item from wishlist on all products page
    """
    product = Album.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item = Wishlist.objects.filter(product=product, user=user)
    wishlist_item.delete()
    messages.success(request, 'Removed from wishlist!!')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'wishlist' in referer:
            return redirect('wishlist')
        else:
            return redirect(referer)
    else:
        return redirect('wishlist')
