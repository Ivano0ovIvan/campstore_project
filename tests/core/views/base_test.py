from django.test import TestCase
from django.urls import reverse

from campstore.store.models import Product, Category, User


class BaseTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.product1 = Product.objects.create(
            title="Test Product 1",
            description="This is a test product.",
            category=self.category, user=self.user,
            price=10
        )
        self.product2 = Product.objects.create(
            title="Test Product 2",
            description="Another test product.",
            category=self.category, user=self.user,
            price=10
        )