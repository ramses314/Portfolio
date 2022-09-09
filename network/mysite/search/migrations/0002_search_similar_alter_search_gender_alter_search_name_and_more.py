# Generated by Django 4.1.1 on 2022-09-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='similar',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='search',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Парень'), ('f', 'Девушка')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
