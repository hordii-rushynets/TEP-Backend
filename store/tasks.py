import os
import requests
from celery import shared_task

from django.core.files.base import ContentFile
from django.core.cache import cache

from urllib.parse import urlparse

from .models import (Category, Color, Filter, FilterField, Material, Product,
                     ProductImage, ProductVariant, ProductVariantImage,
                     ProductVariantInfo, Size)


def get_size(group_offer: dict) -> Size:
    size, _ = Size.objects.get_or_create(
        slug=group_offer.get('size_en').replace(' ', ''),
        title_uk=group_offer.get('size_ua'),
        title_en=group_offer.get('size_en'),
        title_ru=group_offer.get('size_ru')
    )

    return size


def add_product_variant_info(group_offer: dict, product_variant: ProductVariant):
    ProductVariantInfo.objects.get_or_create(
        product_variant=product_variant,
        material_and_care_uk=group_offer.get('description_materials_and_care_ua', 'Empty'),
        material_and_care_en=group_offer.get('description_materials_and_care_en', 'Empty'),
        material_and_care_ru=group_offer.get('description_materials_and_care_ru', 'Empty'),

        ecology_and_environment_uk=group_offer.get('description_ecology_and_environment_ua', 'Empty'),
        ecology_and_environment_en=group_offer.get('description_ecology_and_environment_en', 'Empty'),
        ecology_and_environment_ru=group_offer.get('description_ecology_and_environment_ru', 'Empty'),

        packaging_en=group_offer.get('description_packaging_en', 'Empty'),
        packaging_ru=group_offer.get('description_packaging_ru', 'Empty'),
        packaging_uk=group_offer.get('description_packaging_ua', 'Empty'),
    )

def add_image_of_the_view_in_interior(product: Product, images: list):
    for image in images:
        try:
            # Download the image
            response = requests.get(image)
            if response.status_code == 200:
                parsed_url = urlparse(image)
                filename = os.path.basename(parsed_url.path)
                product_image = ProductImage(product=product)

                product_image.image.save(filename, ContentFile(response.content), save=True)
                
                print({"success": "Image uploaded successfully", "image_id": product_image.id})
            else:
                print({"error": f"Failed to download image, status code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            print({"error": str(e)})

def create_filters(filters: list) -> list:
    for filter in filters:
        created_filter, _ = Filter.objects.get_or_create(name=filter.get('name_ua'))
        created_filter.name_uk = filter.get('name_ua')
        created_filter.name_ru = filter.get('name_ru')
        created_filter.name_en = filter.get('name_en')
        created_filter.save()

        filter['created_filter'] = created_filter

        for value in filter.get('values'):
            filter_field, _ = FilterField.objects.get_or_create(value=value.get('name_ua'), filter=created_filter)
            filter_field.value_uk = value.get('name_ua')
            filter_field.value_ru = value.get('name_ru')
            filter_field.value_en = value.get('name_en')
            filter_field.save()

            value['filter_field'] = filter_field

    return filters

def create_colors(colors: list) -> list:
    for color in colors:
        created_color, _ = Color.objects.get_or_create(slug=color.get('guid'))
        created_color.title_uk = color.get('name_ua')
        created_color.title_ru = color.get('name_ru')
        created_color.title_en = color.get('name_en')
        created_color.save()

        color['created_color'] = created_color

    return colors

def create_categories(categories: list) -> list:
    for category in categories:
        created_category, _ = Category.objects.get_or_create(slug=category.get('name_en').lower().replace(' ', '-').replace("'", ''))
        created_category.title = category.get('name_en')
        created_category.title_uk = category.get('name_ua')
        created_category.title_ru = category.get('name_ru')
        created_category.title_en = category.get('name_en')
        created_category.description_uk = category.get('description_ua')
        created_category.description_ru = category.get('namedescription_ru_ru')
        created_category.description_en = category.get('description_en')

        image = category.get('image')
        response = requests.get(image)
        if response.status_code == 200:
            parsed_url = urlparse(image)
            filename = os.path.basename(parsed_url.path)
            created_category.image.save(filename, ContentFile(response.content), save=True)

        created_category.save()

        category['created_category'] = created_category

    return categories

def get_category_by_slug(slug, categories):
    for category in categories:
        if category["slug"] == slug:
            return category.get('created_category')
    return None

def create_materials(materials: list) -> list:
    result_materials = {}

    for material in materials:
        created_material, _ = Material.objects.get_or_create(slug=material.get('guid'))
        created_material.title_uk = material.get('name_ua')
        created_material.title_rn = material.get('name_en')
        created_material.title_ru = material.get('name_ru')

        created_material.save()

        result_materials[material.get('guid')] = created_material

    return result_materials


def create_product_variant_images(images: list, variant: ProductVariant):
     i = 0
     for image in images:
        try:
            # Download the image
            response = requests.get(image)
            if response.status_code == 200:
                parsed_url = urlparse(image)
                filename = os.path.basename(parsed_url.path)
                product_variant_image = ProductVariantImage(product_variant=variant)

                if i == 0:
                    variant.main_image.save(filename, ContentFile(response.content), save=True)
                    variant.save()

                product_variant_image.image.save(filename, ContentFile(response.content), save=True)
                
                product_variant_image.save()
                print({"success": "Image uploaded successfully", "image_id": product_variant_image.id})
            else:
                print({"error": f"Failed to download image, status code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            print({"error": str(e)})
        
        i+=1


@shared_task(time_limit=3600*3, soft_time_limit=3500*3)
def import_data_task(data):
    print(data.get('filters'))
    filters = create_filters(data.get('filters'))
    categories = create_categories(data.get('categories'))
    materials = create_materials(data.get('components'))
    create_colors(data.get('colors'))

    offers = data.get('offers', [])
    for offer in offers:
        group_id = offer.get('group_id')
        group_name_en = offer.get('group_name_en', '')
        group_offers = offer.get('group_offers', [])

        description_en = offer.get('description_en', '')
        description_ru = offer.get('description_ru', '')
        description_uk = offer.get('description_ua', '')

        product, created = Product.objects.get_or_create(
            group_id=group_id,
            defaults={
                'title': group_name_en,
                'description': description_uk,
                'slug': group_id,
                'dimensional_grid_description': ''
            }
        )

        product.title_uk = offer.get('group_name_ua', '')
        product.title_en = offer.get('group_name_en', '')
        product.title_ru = offer.get('group_name_ru', '')

        product.description_en = description_en
        product.description_uk = description_uk
        product.description_ru = description_ru
        product.category = get_category_by_slug(offer.get('category'), categories)

        product.save()

        for group_offer in group_offers:
            if not group_offer:
                continue

            article = group_offer.get('article')
            name_en = group_offer.get('name_en')
            group_order = group_offer.get('group_order')
            price = group_offer.get('price', 0)
            price_1 = group_offer.get('price_1', 0)
            price_2 = group_offer.get('price_2', 0)
            count = group_offer.get('count', 0)

            size = get_size(group_offer)

            variant, created = ProductVariant.objects.get_or_create(
                product=product,
                sku=article,
                defaults={
                    'title': name_en,
                    'default_price': price,
                    'wholesale_price': price_1,
                    'drop_shipping_price': price_2,
                    'count': count,
                    'variant_order': group_order
                }
            )
            variant.title_uk = group_offer.get('name_ua')
            variant.title_en = name_en
            variant.title_ru = group_offer.get('name_ru')

            variant.sizes.add(size)
            colors = group_offer.get('color') if group_offer.get('color') else []
            for color in colors:
                try:
                    created_color = Color.objects.get(slug=color)
                    variant.colors.add(created_color)
                except Color.DoesNotExist:
                    continue

            for filter in filters:
                filter_fields = group_offer.get(filter['slug'], [])
                for filter_field in filter_fields:
                    result = next((value for value in filter.get('values') if value['guid'] == filter_field), None)
                    variant.filter_field.add(result['filter_field'])

            for material in group_offer.get('components'):
                created_material = materials.get(material)
                if created_material: variant.materials.add(created_material)

            variant.save()
            images = group_offer.get('images') if group_offer.get('images') else []
            create_product_variant_images(images, variant)
            add_product_variant_info(group_offer, variant)


save_queryset_key = 'product_queryset_key'


@shared_task
def save_queryset():
    queryset = Product.objects.all()
    cache.set(save_queryset_key, queryset, timeout=10800)
