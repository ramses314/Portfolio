# Generated by Django 4.1.1 on 2022-09-09 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Парень'), ('f', 'Девушка')], max_length=1, null=True),
        ),
    ]
