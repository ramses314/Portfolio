# Generated by Django 4.1.4 on 2023-03-21 14:34

import applications.core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='published', max_length=50, verbose_name='Status')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='published', max_length=50, verbose_name='Status')),
                ('request_id', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='published', max_length=50, verbose_name='Status')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Slug')),
                ('counter', models.IntegerField(default=0, verbose_name='counter')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
                ('on_landing', models.BooleanField(default=False, verbose_name='On Landing')),
                ('content', models.TextField(verbose_name='Content')),
                ('expired', models.DateTimeField(verbose_name='Expired')),
                ('image', models.ImageField(blank=True, null=True, upload_to=applications.core.models.PathAndRename('events/event/image'), verbose_name='Image')),
                ('ticket_quantity', models.BigIntegerField(default=0, verbose_name='Ticket quantity')),
                ('link', models.CharField(max_length=500, verbose_name='Translation link')),
                ('time_event', models.TimeField(blank=True, null=True, verbose_name='Time to event')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='published', max_length=50, verbose_name='Status')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('image', models.ImageField(blank=True, null=True, upload_to=applications.core.models.PathAndRename('events/prize/image'), verbose_name='Image')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prizes', to='events.event', verbose_name='Event')),
            ],
            options={
                'verbose_name': 'prize',
                'verbose_name_plural': 'prizes',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Unique id')),
                ('status', models.CharField(choices=[('sold', 'sold'), ('blocked', 'blocked'), ('open', 'open')], default='open', max_length=50, verbose_name='Status')),
                ('number', models.BigIntegerField(verbose_name='Number')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to=applications.core.models.PathAndRename('events/ticket/qr_code'), verbose_name='QR')),
                ('is_winner', models.BooleanField(default=False, verbose_name='Winner?')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='events.event', verbose_name='Event')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='sales.order', verbose_name='Order')),
                ('prize_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prize', to='events.prize', verbose_name='prize_id')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
        ),
    ]
