# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models
from django.contrib.auth.models import User
# Internal:
from products.models import Album
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Wishlist(models.Model):
    """
    Model for users to save their favoutite
    products to a wishlist
    """
    product = models.ForeignKey(
        Album,
        related_name='wishlist',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='wishlist',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.product.name
