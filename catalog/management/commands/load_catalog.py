import json
from typing import Any

from django.core.management.base import BaseCommand

from catalog.models import Category, Contact, Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Наполняет данными таблицы приложения catalog"

    @staticmethod
    def __get_data() -> dict:
        """Получение данных из файла фикстуры fixture/fixture_catalog.json"""

        with open("fixture/fixture_catalog.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
        raise ValueError("Некорректная структура данных!")

    @staticmethod
    def __load_products(cat_id: int, data: list) -> None:
        """Сохраняет в БД информацию о продуктах"""

        for i in data:
            product_category = i.get("category")
            if product_category == cat_id:
                i["category"] = Category.objects.get(pk=cat_id)
                owner_email = i.pop("owner")
                i["owner"] = CustomUser.objects.get(email=owner_email)
                product, created = Product.objects.get_or_create(**i)
                if created:
                    print(f"Новый продукт <{product.name}> добавлен в базу данных.")
                else:
                    print(f"В базе данных уже существует продукт <{product.name}>.")

    def __load_categories(self, data: dict) -> None:
        """Сохраняет в БД информацию о категориях продуктов"""

        categories = data.get("categories", dict())
        for cat_id, content in categories.items():
            category, created = Category.objects.get_or_create(**content)
            if created:
                print(f"\nСоздана новая категория продуктов <{category.name}>.")
            else:
                print(
                    f"\nКатегория <{category.name}> уже существует в базе данных, возможно, "
                    + "она будет дополнена некоторым списком продуктов"
                )
            products_data = data.get("products", list())
            self.__load_products(int(cat_id), products_data)

    @staticmethod
    def __load_contacts(data: list) -> None:
        """Сохраняет в БД контакты пользователей"""

        for i in data:
            contact, created = Contact.objects.get_or_create(**i)
            if created:
                print(f"В базу данных добавлены контактные данные <{contact.name}>.")
            else:
                print(f"В базе данных уже существуют контактные данные <{contact.name}>.")

    def handle(self, *args: Any, **options: Any) -> None:
        """Вызов команды из терминала"""

        try:
            data = self.__get_data()
            self.__load_categories(data)
            self.__load_contacts(data.get("contacts", list()))
        except FileNotFoundError:
            print("Файл фикстуры fixture/fixture_catalog.json не обнаружен.")
