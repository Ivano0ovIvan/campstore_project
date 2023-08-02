from django.test import TestCase


class PageNotFoundViewTest(TestCase):
    def test_page_not_found_view(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')