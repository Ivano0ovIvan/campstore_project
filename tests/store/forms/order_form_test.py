from django.test import TestCase

from campstore.store.forms import OrderForm


class OrderFormTest(TestCase):
    def test_valid_order_form(self):
        data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'address': 'Varna bul. Vl. Varnenchic',
            'post_code': '12345',
            'phone_number': '887772893499'
        }
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_order_form(self):
        data = {
            'first_name': 'Ivan',
            'last_name': '',
            'address': 'Varna bul. Vl. Varnenchic',
            'post_code': '12345',
            'phone_number': '555-1234'
        }
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())