# Generated by Django 4.2.2 on 2024-07-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_productvariant_filter_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='colors',
            field=models.ManyToManyField(blank=True, to='store.color'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='filter_field',
            field=models.ManyToManyField(related_name='filter', to='store.filterfield'),
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