from tests.core.views.base_test import BaseTestCase
from django.urls import reverse


class SearchViewTest(BaseTestCase):
    def test_search_view_with_results(self):
        response = self.client.get(reverse('search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "Test Product 2")
        self.assertNotContains(response, "Random Product")