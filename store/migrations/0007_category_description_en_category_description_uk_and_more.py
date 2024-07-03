# Generated by Django 5.0.2 on 2024-03-30 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_price_productvariant_default_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_uk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_uk',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='color',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='color',
            name='title_uk',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_uk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_uk',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='title_uk',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='ecology_and_environment_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='ecology_and_environment_uk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='material_and_care_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='material_and_care_uk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='packaging_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariantinfo',
            name='packaging_uk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='size',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='size',
            name='title_uk',
            field=models.CharField(max_length=128, null=True),
        ),
    ]