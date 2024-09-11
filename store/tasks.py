from celery import shared_task
from .models import Product, ProductVariant

@shared_task
def import_data_task(data):
    offers = data.get('offers', [])
    for offer in offers:
        group_id = offer.get('group_id')
        group_name_en = offer.get('group_name_en', '')
        group_offers = offer.get('group_offers', [])

        product, created = Product.objects.get_or_create(
            group_id=group_id,
            defaults={'title': group_name_en}
        )

        for group_offer in group_offers:
            article = group_offer.get('article')
            name = group_offer.get('name')
            group_order = group_offer.get('group_order')
            price = group_offer.get('price', 0)
            price_1 = group_offer.get('price_1', 0)
            price_2 = group_offer.get('price_2', 0)
            count = group_offer.get('count', 0)
            description_en = group_offer.get('description_en', '')
            description_materials_en = group_offer.get('description_materials_en', '')
            description_materials_ua = group_offer.get('description_materials_ua', '')
            description_materials_ru = group_offer.get('description_materials_ru', '')

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
                    'description': description_en,
                    'description_materials_en': description_materials_en,
                    'description_materials_ru': description_materials_ru,
                    'description_materials_ua': description_materials_ua
                }
            )
