# Generated by Django 4.0.3 on 2022-03-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_alter_product_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeproduct',
            name='certainty',
        ),
        migrations.AddField(
            model_name='product',
            name='certainty',
            field=models.FloatField(default=0),
        ),
    ]