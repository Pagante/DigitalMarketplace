# Generated by Django 3.2 on 2022-04-24 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpurchase',
            old_name='product',
            new_name='products',
        ),
    ]
