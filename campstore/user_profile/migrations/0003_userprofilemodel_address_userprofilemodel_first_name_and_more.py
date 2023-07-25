# Generated by Django 4.2.3 on 2023-07-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_userprofilemodel_is_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='post_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='profile_picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
