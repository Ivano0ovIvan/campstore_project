# Generated by Django 4.2.3 on 2023-07-31 07:21

import campstore.store.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, validators=[campstore.store.validators.validate_positive_number]),
        ),
    ]
