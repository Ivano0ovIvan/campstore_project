from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO
from PIL import Image

from campstore.store.validators import validate_positive_number, validate_name, validate_name_length, \
    validate_phone_number


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


def create_unique_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    if Product.objects.filter(slug=slug).exists():
        random_string = get_random_string(length=4)
        slug = f"{slug}-{random_string}"
        return create_unique_slug(instance, new_slug=slug)
    return slug


class Product(models.Model):
    SOLD_OUT = 'sold_out'
    WAITING_APPROVAL = 'waiting_approval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (SOLD_OUT, 'Sold out'),
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

    title = models.CharField(
        max_length=50,
        validators=[validate_name, validate_name_length])
    slug = models.SlugField(
        max_length=40,
        unique=True,
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.IntegerField(validators=[validate_positive_number])
    main_image = models.ImageField(
        upload_to='uploads/product_images/',
        blank=True,
        null=True
    )
    images = models.ManyToManyField(
        'ProductImage',
        blank=True,
        related_name='products_related',
    )
    quantity = models.IntegerField(default=1, validators=[validate_positive_number])
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
        self.slug = create_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_display_price(self):
        return f'{self.price:.2f}'

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.main_image:
                self.thumbnail = self.make_thumbnail(self.main_image)
                self.save()

                return self.thumbnail.url
            else:
                return 'static/images/no_image.jpg'

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        if img.mode == 'P':
            img = img.convert('RGB')
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='images_related'
                                )
    image = models.ImageField(
        upload_to='uploads/product_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image for {self.product.title}"


class Order(models.Model):
    first_name = models.CharField(validators = [validate_name, validate_name_length],max_length=50)
    last_name = models.CharField(validators = [validate_name, validate_name_length],max_length=50)
    address = models.CharField(max_length=200)
    post_code = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[validate_phone_number],max_length=15)
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
    quantity = models.IntegerField(default=1, validators=[validate_positive_number])

    def get_order_price(self):
        return f'{self.price:.2f}'