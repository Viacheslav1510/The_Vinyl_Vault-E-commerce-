# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
# Internal:
from .models import Album, Genre, Review
from .forms import AlbumForm, ReviewForm
from wishlist.models import Wishlist
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def all_products(request):
    """
    A function to provide all products list,
    provide sorting and searching,
    pass wishlist
    """
    albums = Album.objects.all()
    query = None
    genre = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sort_key = request.GET['sort']
            sort = sort_key
            if sort_key == 'genre':
                sort_key = 'genre__name'
            if sort_key == 'name':
                sort_key = 'lower_name'
                albums = albums.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort_key = f'-{sort_key}'
            albums = albums.order_by(sort_key)

        if 'genre' in request.GET:
            genres = request.GET['genre'].split(',')
            albums = albums.filter(genre__name__in=genres)
            genres = Genre.objects.filter(name__in=genres)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | \
                Q(description__icontains=query)
            albums = albums.filter(queries)

    user = request.user
    wished_list = []
    if user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=user)
        for i in wishlist:
            wished_list.append(i.product)
    current_sort = f'{sort}_{direction}'
    context = {
        'albums': albums,
        'search_term': query,
        'current_sort': current_sort,
        'wished_list': wished_list,

    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A fucntion to render product details page,
    handle wishlist functionality
    """
    album = get_object_or_404(Album, pk=product_id)
    user = request.user
    in_wishlist = False
    wishlist_item = None
    tracks = album.tracks.all()
    reviews = Review.objects.filter(product=album)
    form = ReviewForm(request.POST)

    if user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(
            product=album, user=user).first()
        in_wishlist = Wishlist.objects.filter(
            product=album, user=user).exists()

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.product = album
                form.save()
                messages.info(request, "You've left the review successfully")
                return redirect(reverse('product_detail', args=[product_id]))

    context = {
        'album': album,
        'tracks': tracks,
        'in_wishlist': in_wishlist,
        'wishlist_item': wishlist_item,
        'form': form,
        'reviews': reviews
    }
    return render(request, 'products/product_detail.html', context)


@login_required()
def edit_review(request, review_id):
    """Edit a review"""

    review = get_object_or_404(Review, pk=review_id)
    album = review.product

    if request.user != review.user:
        messages.error(request, 'No no no! I knew that you could do it!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Review successfully updated!')
            return redirect(reverse('product_detail', args=[album.id]))
        else:
            messages.error(
                request, 'Failed to update this review. \
                    Please ensure the form is valid.')
    else:
        form = ReviewForm(instance=review)
        messages.info(request, 'You are editing your review')

    template = 'products/edit_review.html'

    context = {
        'form': form,
        'review': review,
        'album': album,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """ Delete review from the product details page """
    review = get_object_or_404(Review, pk=review_id)
    album = review.product

    if request.user != review.user:
        messages.error(request, 'No no no! I knew that you could do it!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted!')
        return redirect(reverse('product_detail', args=[album.id]))

    return render(request, 'products/delete_review.html')


@login_required
def add_product(request):
    """
    A function to add a product to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'How dare you? Only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Failed to add product. \
                           Please ensure the form is valid.')
    else:
        form = AlbumForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    A function to edit a product in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'How dare you? Only store owners can do that.')
        return redirect(reverse('home'))

    album = get_object_or_404(Album, pk=product_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Failed to update product. \
                            Please ensure the form is valid.')
    else:
        form = AlbumForm(instance=album)
        messages.info(request, f'You are editing {album.name}')

    template = 'products/update_product.html'
    context = {
        'form': form,
        'album': album,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    A function to delete a product from the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'How dare you? Only store owners can do that.')
        return redirect(reverse('home'))

    album = get_object_or_404(Album, pk=product_id)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))
    template = 'products/delete-confirmation.html'
    context = {
        'album': album,
    }
    return render(request, template, context)
