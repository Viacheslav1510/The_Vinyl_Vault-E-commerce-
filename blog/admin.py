# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Internal:
from .models import Post
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@admin.register(Post)
class PostModelAdmin(SummernoteModelAdmin):
    """
    A class to register post model in admin panel
    """
    summernote_fields = ('content')
    list_filter = (
        'title',
        'date_created',
        )
    list_display = ('title', 'date_created')
    search_fields = ['title']
