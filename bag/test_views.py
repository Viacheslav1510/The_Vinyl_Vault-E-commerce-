# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase, Client
# Internal:
from products.models import Album, Genre
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestBagViews(TestCase):
    """
    A class for all bag views tests
    """
    def setUp(self):
        self.client = Client()
        self.album = Album.objects.create(
            name='Test Album',
            image='img.jpg',
            price=9.99
        )
        self.bag_url = reverse('bag')
        self.add_to_bag_url = reverse('add_to_bag', args=[self.album.id])
        self.adjust_bag_url = reverse('adjust_bag', args=[self.album.id])
        self.remove_from_bag_url = reverse(
                                    'remove_from_bag',
                                    args=[self.album.id]
                                )

    def test_get_bag_view(self):
        """
        a test to get bag template
        """
        response = self.client.get(self.bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('bag/bag.html')

    def test_add_to_bag_view(self):
        """
        a test to add product to bag
        """
        data = {
            'quantity': 1,
            'redirect_url': '/bag/'
        }
        response = self.client.post(self.add_to_bag_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bag/')
        self.assertEqual(len(self.client.session['bag']), 1)

    def test_adjust_bag_view(self):
        """
        a test to update product in bag
        """
        data = {
            'quantity': 3,
            'redirect_url': '/bag/'
        }
        response = self.client.post(self.adjust_bag_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bag/')
        self.assertEqual(self.client.session['bag'][str(self.album.id)], 3)

    def test_adjust_bag_view_quantity_less_than_1(self):
        """
        a test to update product with product quantity less than 1
        """
        data = {
            'quantity': -1,
            'redirect_url': '/bag/'
        }
        response = self.client.post(self.adjust_bag_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bag/')
        self.assertEqual(self.client.session['bag'][str(self.album.id)], 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "You can't choose less than 1"
        )

    def test_remove_from_bag_view(self):
        """
        a test to remove product from bag
        """
        data = {
            'quantity': 1,
            'redirect_url': '/bag/'
        }
        self.client.post(self.add_to_bag_url, data=data)
        response = self.client.post(self.remove_from_bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session['bag']), 0)

    def test_remove_from_bag_view_fail(self):
        """
        a test to fail remove product from bag
        """
        response = self.client.post(self.remove_from_bag_url)
        self.assertEqual(response.status_code, 500)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            f"Error removing item '{self.album.id}'"
        )
