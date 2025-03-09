# Generated by Django 5.0.6 on 2024-07-17 18:23

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_delete_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ecommerce/order/image')),
                ('product', models.CharField(default='', max_length=1000)),
                ('price', models.IntegerField()),
                ('quantity', models.CharField(max_length=5)),
                ('size', models.CharField(max_length=3)),
                ('total', models.CharField(default='', max_length=1000)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('pincode', models.CharField(max_length=10)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
