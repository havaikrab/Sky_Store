import json
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет все существующие данные модели Product и заполняет таблицу данными из фикстуры"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--fixture", type=str, help="Путь к файлу с фикстурой")

    def __read_fixture_write_data(self, path_to_file: str) -> None:
        """Метод, читающий данные для записи из фикстуры"""

        products = list()
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                products = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл {path_to_file} не найден"))

        for element in products:
            fields = element.get("fields", dict())
            category_id = fields.get("category")
            fields["category"] = Category.objects.get(id=category_id)
            product, created = Product.objects.get_or_create(**fields)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Продукт {product} успешно добавлен в базу данных"))

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Метод, исполняющий команду"""

        Product.objects.all().delete()
        path_to_fixture = kwargs.get("fixture", "")
        self.__read_fixture_write_data(path_to_fixture)
