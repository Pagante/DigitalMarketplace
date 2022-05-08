# Generated by Django 3.2 on 2022-04-24 08:51

import django.core.files.storage
from django.db import migrations, models
import pathlib
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='download',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location=pathlib.PureWindowsPath('C:/Users/SONY/Desktop/DigiMkt/static/protected')), upload_to=products.models.download_loc),
        ),
    ]