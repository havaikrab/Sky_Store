import json
from typing import Any

from django.core.management.base import BaseCommand

from sky_blog.models import Article


class Command(BaseCommand):
    help = "Наполняет данными таблицы приложения sky_blog"

    @staticmethod
    def __load_data() -> None:
        """Получение данных из файла фикстуры fixture/fixture_sky_blog.json и запись данных в таблицу модели Article"""

        with open("fixture/fixture_sky_blog.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        articles = data.get("articles")
        loads_count = 0
        for article_dict in articles:
            article = Article.objects.get_or_create(**article_dict)
            if article[1]:
                loads_count += 1
        print(f"Создано '{loads_count}' новых объектов модели sky_blog.Article")

    def handle(self, *args: Any, **options: Any) -> None:
        """Вызов команды из терминала"""

        try:
            self.__load_data()
        except FileNotFoundError:
            print("Файл фикстуры fixture/fixture_sky_blog.json не обнаружен.")
