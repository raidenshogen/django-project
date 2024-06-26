# Generated by Django 5.0.6 on 2024-05-22 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="height_field",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="width_field",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]
