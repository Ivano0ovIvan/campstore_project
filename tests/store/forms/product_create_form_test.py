from django.test import TestCase

from campstore.store.forms import ProductCreateForm
from campstore.store.models import Category


class ProductCreateFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')

    def test_valid_product_create_form(self):
        data = {
            'category':  self.category.id,
            'title': 'Test Product',
            'description': 'This is a test product.',
            'price': 20.50,
            'main_image': None,
            'quantity': 10
        }
        form = ProductCreateForm(data=data, files={'images': []})
        self.assertTrue(form.is_valid())

    def test_invalid_product_create_form(self):
        data = {
            'category': '',
            'title': '',
            'description': 'This is a test product.',
            'price': 20.50,
            'main_image': None,
            'quantity': -5
        }
        form = ProductCreateForm(data=data, files={'images': []})
        self.assertFalse(form.is_valid())