# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import path
# Internal:
from . import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path(
        'add_to_wishlist/<int:product_id>/<int:user_id>',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'remove_from_wishlist/<int:wishlist_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),
    path(
        'add_to_wishlist_all/<int:product_id>/<int:user_id>',
        views.add_to_wishlist_all_products,
        name='add_to_wishlist_all'
    ),
    path(
        'remove_from_wishlist_all/<int:product_id>/<int:user_id>',
        views.remove_from_wishlist_all,
        name='remove_from_wishlist_all'
    ),
]
