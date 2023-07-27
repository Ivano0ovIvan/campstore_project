# Generated by Django 4.2.3 on 2023-07-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofilemodel_address_userprofilemodel_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_images/'),
        ),
    ]
