from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from common.models import TitleSlug
from tep_user.models import TEPUser
from django.utils import timezone

from django.db.models import Avg


class Filter(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class FilterField(models.Model):
    value = models.CharField(max_length=128, blank=True, null=True)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, related_name='filter_field', blank=True, null=True)

    def __str__(self):
        return self.value


class Category(TitleSlug):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    filter = models.ManyToManyField(Filter, related_name='filter')

    def __str__(self):
        return self.title


class Product(TitleSlug):
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    group_id = models.CharField(max_length=128)
    last_modified = models.DateTimeField(auto_now=True)
    number_of_views = models.IntegerField(default=0, validators=[MinValueValidator(0),])

    def __str__(self):
        return str(self.slug)

    def get_average_rating(self):
        average_rating = self.feed_back.aggregate(average=Avg('evaluation'))['average']
        return average_rating if average_rating is not None else 0


class ProductImage(models.Model):
    """Product image Model"""
    image = models.ImageField(upload_to='product/images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True)


class FavoriteProduct(models.Model):
    user = models.ForeignKey(TEPUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.email} - {self.product.title} - favorite: {self.favorite}.'


class DimensionalGrid(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dimensional_grid')

    def __str__(self) -> str:
        return self.title


class DimensionalGridSize(models.Model):
    title = models.CharField(max_length=255)
    size = models.CharField(max_length=255)

    dimensional_grid = models.ForeignKey(DimensionalGrid, on_delete=models.CASCADE, related_name='sizes')

    def __str__(self) -> str:
        return f'{self.title} - {self.size}'


class Size(TitleSlug):
    def __str__(self):
        return self.title


class Color(TitleSlug):
    hex = models.CharField(max_length=12)

    def __str__(self):
        return self.title


class Material(TitleSlug):

    def __str__(self):
        return self.title


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    title = models.CharField(max_length=128)
    sku = models.CharField(max_length=100, unique=True)
    default_price = models.IntegerField(default=0)
    wholesale_price = models.IntegerField(default=0)
    drop_shipping_price = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    materials = models.ManyToManyField(Material, blank=True)
    main_image = models.ImageField(upload_to='products/images/', blank=True)
    promotion = models.BooleanField(default=False)
    promo_price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    variant_order = models.IntegerField(default=0)
    filter_field = models.ManyToManyField(FilterField, related_name='product_variants')

    def __str__(self):
        return str(self.sku)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class ProductVariantInfo(models.Model):
    material_and_care = models.TextField()
    ecology_and_environment = models.TextField()
    packaging = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    product_variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='variant_info')

    def __str__(self):
        return self.product_variant.product.title


class ProductVariantImage(models.Model):
    image = models.ImageField(upload_to='products/images/', blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_images')


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


class Feedback(models.Model):
    """Feedback Model"""
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, related_name='feed_back')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feed_back')
    text = models.TextField(blank=True, null=True)
    like_number = models.PositiveIntegerField(default=0)
    dislike_number = models.PositiveIntegerField(default=0)
    evaluation = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5),])
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tep_user.email} + {self.product.slug}"

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None

        try:
            vote = self.votes.get(tep_user=user)
            return vote.is_like
        except FeedbackVote.DoesNotExist:
            return None


class FeedbackImage(models.Model):
    """Feedback image Model"""
    image = models.ImageField(upload_to='feedback/images/', blank=True)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='feedback_images', null=True)


class FeedbackVote(models.Model):
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='votes')
    is_like = models.BooleanField(null=True)

    class Meta:
        unique_together = ('tep_user', 'feedback')

    def __str__(self):
        return f"{self.tep_user.email} {self.feedback.product.slug} {self.is_like}"