# Generated by Django 4.0.3 on 2022-04-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_remove_product_certainty_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]
