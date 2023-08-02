from django.test import TestCase
from campstore.user_profile.models import User
from campstore.store.models import Order


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.order = Order.objects.create(
            first_name='Ivan',
            last_name='Ivanov',
            address='Varna',
            post_code='12345',
            phone_number='235346457',
            paid_amount=100,
            is_paid=True,
            seller_id='seller123',
            created_by=cls.user
        )

    def test_first_name_max_length(self):
        order = self.order
        max_length = order._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        order = self.order
        max_length = order._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_paid_amount_blank_null(self):
        order = self.order
        self.assertEquals(order.paid_amount, 100)

    def test_is_paid_default(self):
        order = self.order
        self.assertTrue(order.is_paid)

