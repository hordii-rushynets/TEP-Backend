# Generated by Django 4.2.2 on 2024-07-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_filterfield_category_image_product_last_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='colors',
            field=models.ManyToManyField(blank=True, to='store.color'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='materials',
            field=models.ManyToManyField(blank=True, to='store.material'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='store.size'),
        ),
    ]