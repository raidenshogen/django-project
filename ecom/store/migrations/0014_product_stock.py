# Generated by Django 5.0.6 on 2024-05-28 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0013_alter_product_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=0),
        ),
    ]