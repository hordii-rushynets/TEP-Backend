# Generated by Django 4.2.2 on 2024-07-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_productvariantimage_product_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='filter_field',
            field=models.ManyToManyField(related_name='filter_field', to='store.filterfield'),
        ),
    ]
