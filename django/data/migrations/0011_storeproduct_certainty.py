# Generated by Django 4.0.3 on 2022-03-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_remove_price_end_storeproduct_has_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproduct',
            name='certainty',
            field=models.FloatField(default=0),
        ),
    ]