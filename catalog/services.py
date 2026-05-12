from typing import Optional

from django.core.cache import cache
from django.db.models import QuerySet

from catalog.models import Product


def get_products(category_id: Optional[int] = None) -> QuerySet:
    """Возвращает соответствующий список продуктов из кеша или из базы данных"""

    key = "products"
    if category_id:
        key += f"_by_category_{category_id}"
    else:
        key += "_all"
    products_list: Optional[QuerySet] = cache.get(key)
    if products_list is None:
        if category_id:
            products_list = Product.objects.filter(category_id=category_id, is_published=True)
        else:
            products_list = Product.objects.filter(is_published=True)
        cache.add(key, products_list, 60)
    return products_list
