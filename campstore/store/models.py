from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(
        max_length=40,
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=40)
    slug = models.SlugField(
        max_length=40,
        unique=True,
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to='uploads/product_images/',
        blank=True,
        null=True
    )
    thumbnail = models.ImageField(
        upload_to='uploads/product_images/thumbnail/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_display_price(self):
        return f'{self.price:.2f}'

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'static/images/no_image.jpg'

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail


class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    post_code = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    seller_id = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_order_price(self):
        return f'{self.price:.2f}'