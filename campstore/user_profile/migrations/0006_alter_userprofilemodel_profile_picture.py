# Generated by Django 4.2.3 on 2023-07-27 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_alter_userprofilemodel_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_images'),
        ),
    ]