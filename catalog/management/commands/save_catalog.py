import json
from typing import Any

from django.core.management.base import BaseCommand

from catalog.models import Category, Contact, Product


class Command(BaseCommand):
    help = "Сохраняет текущее состояние базы данных для приложения catalog"

    @staticmethod
    def __save_categories() -> dict:
        """Получение всех существующих в БД категорий продуктов"""

        categories_dict = dict()
        for cat in Category.objects.all():
            categories_dict.update({cat.pk: {"name": cat.name, "description": cat.description}})
        return categories_dict

    @staticmethod
    def __save_products() -> list:
        """Получение всех продуктов, существующих в БД"""

        products_list = list()
        for prod in Product.objects.all():
            products_list.append(
                {
                    "name": prod.name,
                    "description": prod.description,
                    "photo": prod.photo.name,
                    "category": prod.category.pk,
                    "price": prod.price,
                    "is_published": prod.is_published,
                    "owner": prod.owner.email,
                }
            )
        return products_list

    @staticmethod
    def __save_contacts() -> list:
        """Получение всех контактов, существующих в БД"""

        contacts_list = list()
        for cont in Contact.objects.all():
            contacts_list.append({"name": cont.name, "phone": cont.phone, "message": cont.message})
        return contacts_list

    def handle(self, *args: Any, **options: Any) -> None:
        """Запись данных приложения catalog в файл fixture/fixture_catalog.json"""

        data: dict = dict()
        data["categories"] = self.__save_categories()
        data["products"] = self.__save_products()
        data["contacts"] = self.__save_contacts()
        with open("fixture/fixture_catalog.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
