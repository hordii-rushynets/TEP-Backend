# Generated by Django 5.0.2 on 2024-02-13 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='product_variant',
        ),
        migrations.RemoveField(
            model_name='material',
            name='product_variant',
        ),
        migrations.RemoveField(
            model_name='size',
            name='product_variant',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='colors',
            field=models.ManyToManyField(to='store.color'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='materials',
            field=models.ManyToManyField(to='store.material'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='sizes',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]