# Generated by Django 4.2.3 on 2023-07-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_rename_zipcode_order_post_code_remove_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.ImageField(default=1, upload_to=''),
        ),
    ]