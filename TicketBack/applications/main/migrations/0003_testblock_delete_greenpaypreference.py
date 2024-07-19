# Generated by Django 4.1.4 on 2023-06-09 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_preference_front_url_preference_google_redirect_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_expired', models.BooleanField(default=True, verbose_name='Order expired')),
            ],
            options={
                'verbose_name': 'Testing block',
                'verbose_name_plural': 'Testing block',
            },
        ),
        migrations.DeleteModel(
            name='GreenpayPreference',
        ),
    ]