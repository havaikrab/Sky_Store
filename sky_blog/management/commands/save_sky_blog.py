import json
from typing import Any

from django.core.management.base import BaseCommand

from sky_blog.models import Article


class Command(BaseCommand):
    help = "Сохраняет текущее состояние базы данных для приложения sky_blog"

    @staticmethod
    def __save_articles() -> list:
        """Получение всех статей, существующих в БД"""

        articles_list = list()
        for article in Article.objects.all():
            articles_list.append(
                {
                    "title": article.title,
                    "content": article.content,
                    "preview": article.preview.name,
                    "is_published": article.is_published,
                    "views_count": article.views_count,
                }
            )
        return articles_list

    def handle(self, *args: Any, **options: Any) -> None:
        """Запись данных приложения sky_blog в файл fixture/fixture_sky_blog.json"""

        data: dict = dict()
        data["articles"] = self.__save_articles()
        with open("fixture/fixture_sky_blog.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
