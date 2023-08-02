from tests.core.views.base_test import BaseTestCase
from django.urls import reverse

from campstore.store.models import Category


class CategoryDetailsViewTest(BaseTestCase):
    def test_category_details_view_with_products(self):
        response = self.client.get(reverse('category-details', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "Test Product 2")

    def test_category_details_view_no_products(self):
        empty_category = Category.objects.create(title="Empty Category")
        response = self.client.get(reverse('category-details', kwargs={'slug': empty_category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empty Category")

    def test_category_details_view_nonexistent_category(self):
        response = self.client.get(reverse('category-details', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)