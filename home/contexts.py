# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
# Internal:
from products.models import Genre
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def genres_contents(request):
    """
    A function to provide genres list through all website pages
    """
    genres_list = Genre.objects.all()

    context = {
        'genres_list': genres_list,
    }
    return context
