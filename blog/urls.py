# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import path
# Internal:
from . import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


urlpatterns = [
    path('', views.blog_home, name='blog'),
    path('<int:post_id>', views.post_details, name='post-details'),
]
