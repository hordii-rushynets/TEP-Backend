from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    slug = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    slug = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    group_id = models.CharField(max_length=128)

    def __str__(self):
        return  str(self.pk)


class Size(models.Model):
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    hex = models.CharField(max_length=12)

    def __str__(self):
        return self.title


class Material(models.Model):
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    title = models.CharField(max_length=128)
    sku = models.CharField(max_length=100, unique=True)
    default_price = models.IntegerField(default=0)
    wholesale_price = models.IntegerField(default=0)
    drop_shipping_price = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    materials = models.ManyToManyField(Material)
    main_image = models.ImageField(upload_to='products/images/', blank=True)
    promotion = models.BooleanField(default=False)
    promo_price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    variant_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sku)


class ProductVariantInfo(models.Model):
    material_and_care = models.TextField()
    ecology_and_environment = models.TextField()
    packaging = models.TextField()
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class ProductVariantImage(models.Model):
    image = models.ImageField(upload_to='products/images/', blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class PromoCode(models.Model):
    TYPE_CHOICES = (
        ('amount', 'AMOUNT'),
        ('percent', 'PERCENT'),
    )
    code = models.CharField(max_length=128)
    amount = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='percent')
    active = models.BooleanField(default=False)
    products = models.ManyToManyField(ProductVariant)
