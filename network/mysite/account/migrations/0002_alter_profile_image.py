# Generated by Django 4.1 on 2022-08-20 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='media/defaultr/zero_photo.jpg', upload_to='media/%Y/%m/%d'),
        ),
    ]
