# Generated by Django 4.2.3 on 2023-08-01 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_product_images_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='products_related', to='store.productimage'),
        ),
    ]
