# Generated by Django 4.2.2 on 2024-07-15 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_productvariant_filter_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter',
            name='filter_fields',
        ),
        migrations.AddField(
            model_name='filterfield',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='store.filter'),
        ),
    ]
