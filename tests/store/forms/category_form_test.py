from django.test import TestCase

from campstore.store.forms import CategoryForm


class CategoryFormTest(TestCase):
    def test_valid_category_form(self):
        data = {
            'title': 'Test Category'
        }
        form = CategoryForm(data=data)
        self.assertTrue(form.is_valid())