# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from django.contrib.messages import get_messages
import json
# Internal:
from products.models import Album
from .forms import OrderForm
from .models import Order
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestCheckoutViews(TestCase):
    """
    A class to test checkout views
    """
    def setUp(self):
        self.client = Client()
        self.test_album = Album.objects.create(
            name='Test Album',
            image='img.jpg',
            price=59
        )
        self.bag = {'1': 1}
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='testpass123'
        )
        self.valid_test_data = {
                'full_name': 'Test User',
                'email': 'testuser@test.com',
                'phone_number': '12345678',
                'address1': '12 Test Street',
                'address2': 'Test Address',
                'postcode': 'TE54T1',
                'town_or_city': 'Test City',
                'country': 'US',
                'county': 'Test County',
                'client_secret': 'test_secret',
                'save_info': True
        }
        self.client.login(username='test_user', password='testpass123')
        self.cache_checkout_data_url = reverse('cache_checkout_data')
        self.checkout_url = reverse('checkout')

    def test_checkout_view_get(self):
        """
        A function to test used template for checkout page
        """
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_cache_checkout_data_view(self):
        """
        A function to test caching checkout data
        """
        pid = 'test_pid'
        save_info = 'false'
        bag = self.bag
        with patch('checkout.views.stripe.PaymentIntent.modify') \
                as mock_modify:
            response = self.client.post(self.cache_checkout_data_url, {
                                'client_secret': f'{pid}_secret',
                                'save_info': save_info,
                                'username': self.test_user,
                                'bag': json.dumps(bag)
                            })
            self.assertEqual(response.status_code, 200)
            mock_modify.assert_called_once_with(pid, metadata={
                'bag': json.dumps(bag),
                'save_info': save_info,
                'username': self.test_user,
            })

    def test_checkout_view_with_empty_bag(self):
        """
        A function to test checkout view with empty bag
        """
        self.bag = {}
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.get(self.checkout_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'), status_code=302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "There's nothing in your bag at the moment")

    def test_checkout_and_checkout_success_view(self):
        """
        A function to test checkout view with filled bag
        and test redirect to checkout_success view
        """
        form_data = self.valid_test_data.copy()
        response = self.client.post(reverse('checkout'), data=form_data)
        order = Order.objects.all()[0]
        self.assertRedirects(response, reverse(
            'checkout_success', args=[order.order_number]), status_code=302)
