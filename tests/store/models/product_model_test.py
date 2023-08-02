from django.test import TestCase

from campstore.store.models import Category, Product
from campstore.user_profile.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title='Test Category')
        user = User.objects.create(username='testuser', password='12345')

        cls.product = Product.objects.create(
            category=category,
            user=user,
            title='Test Product',
            price=10.5,
            quantity=5,
            status=Product.ACTIVE
        )

    def test_title_max_length(self):
        product = self.product
        max_length = product._meta.get_field('title').max_length
        self.assertEquals(max_length, 50)

    def test_get_display_price(self):
        product = self.product
        expected_display_price = f'{product.price:.2f}'
        self.assertEquals(product.get_display_price(), expected_display_price)

    def test_get_thumbnail_no_thumbnail(self):
        product = self.product
        thumbnail_url = 'static/images/no_image.jpg'
        self.assertEquals(product.get_thumbnail(), thumbnail_url)

