# Generated by Django 3.2 on 2022-04-24 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity',
        ),
    ]