# Generated by Django 4.0.3 on 2022-04-17 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_remove_storeproduct_certainty_product_certainty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='certainty',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
