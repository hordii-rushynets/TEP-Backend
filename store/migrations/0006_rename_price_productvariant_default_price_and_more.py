import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_promocode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariant',
            old_name='price',
            new_name='default_price',
        ),
        migrations.AddField(
            model_name='product',
            name='group_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productvariant',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='drop_shipping_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='variant_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='wholesale_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='promocode',
            name='products',
            field=models.ManyToManyField(to='store.productvariant'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='sku',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]


