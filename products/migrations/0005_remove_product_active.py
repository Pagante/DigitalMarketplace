# Generated by Django 3.2 on 2022-04-18 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220418_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='active',
        ),
    ]