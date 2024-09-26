import requests
from celery import shared_task
from .models import Product, ProductVariant, Size, ProductVariantInfo, ProductImage, Filter, FilterField, ProductVariantImage, Color
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os


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
        material_and_care_uk=group_offer.get('description_materials_and_care_ua'),
        material_and_care_en=group_offer.get('description_materials_and_care_en'),
        material_and_care_ru=group_offer.get('description_materials_and_care_ru'),

        ecology_and_environment_uk=group_offer.get('description_ecology_and_environment_ua'),
        ecology_and_environment_en=group_offer.get('description_ecology_and_environment_en'),
        ecology_and_environment_ru=group_offer.get('description_ecology_and_environment_ru'),

        packaging_en=group_offer.get('description_packaging_en'),
        packaging_ru=group_offer.get('description_packaging_ru'),
        packaging_uk=group_offer.get('description_packaging_ua'),
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
            filter_field.value_uk = filter.get('name_ua')
            filter_field.value_ru = filter.get('name_ru')
            filter_field.value_en = filter.get('name_en')
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

def create_product_variant_images(images: list, variant: ProductVariant):
     for image in images:
        try:
            # Download the image
            response = requests.get(image)
            if response.status_code == 200:
                parsed_url = urlparse(image)
                filename = os.path.basename(parsed_url.path)
                product_variant_image = ProductVariantImage(product_variant=variant)

                product_variant_image.image.save(filename, ContentFile(response.content), save=True)
                
                print({"success": "Image uploaded successfully", "image_id": product_variant_image.id})
            else:
                print({"error": f"Failed to download image, status code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            print({"error": str(e)})


@shared_task
def import_data_task(data):
    filters = create_filters(data.get('filters'))
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
                'dimensional_grid_description': ''
            }
        )

        product.description_en = description_en
        product.description_uk = description_uk
        product.description_ru = description_ru

        # add_image_of_the_view_in_interior(product, offer.get('images', []))

        for group_offer in group_offers:
            article = group_offer.get('article')
            name = group_offer.get('name')
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
                    'title': name,
                    'default_price': price,
                    'wholesale_price': price_1,
                    'drop_shipping_price': price_2,
                    'count': count,
                    'variant_order': group_order,
                }
            )

            variant.sizes.add(size)
            for color in group_offer.get('color'):
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


            create_product_variant_images(group_offer.get('images'), variant)
            add_product_variant_info(group_offer, variant)