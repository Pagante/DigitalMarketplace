# Generated by Django 3.2 on 2022-04-24 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_rename_product_userpurchase_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpurchase',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
