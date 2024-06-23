from celery import shared_task
from .models import Product, ProductVariant

@shared_task
def import_data_task(data):
    offers = data.get('offers', [])
    for offer in offers:
        group_id = offer.get('group_id')
        group_name = offer.get('group_name')
        group_offers = offer.get('group_offers', [])
        product, created = Product.objects.get_or_create(
            group_id=group_id,
            defaults={'title': group_name}
        )
        for group_offer in group_offers:
            article = group_offer.get('article')
            name = group_offer.get('name')
            group_order = group_offer.get('group_order')
            price = group_offer.get('price')
            price_1 = group_offer.get('price_1')
            price_2 = group_offer.get('price_2')
            count = group_offer.get('count')
            variant, created = ProductVariant.objects.get_or_create(
                product=product,
                sku=article,
                defaults={
                    'title': name,
                    'default_price': price,
                    'wholesale_price': price_1,
                    'drop_shipping_price': price_2,
                    'count': count,
                    'variant_order': group_order
                }
            )