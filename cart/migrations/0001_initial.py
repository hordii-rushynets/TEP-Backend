# Generated by Django 4.2.2 on 2024-07-12 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0010_alter_productvariant_colors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_variants', models.ManyToManyField(blank=True, related_name='product_variants', to='store.productvariant')),
                ('tep_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tep_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
