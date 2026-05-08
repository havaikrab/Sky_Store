import json
from typing import Any

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Наполняет данными таблицы приложения users"

    @staticmethod
    def __get_data() -> dict:
        """Получение данных из файла фикстуры fixture/fixture_users.json"""

        with open("fixture/fixture_users.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
        raise ValueError("Некорректная структура данных!")

    @staticmethod
    def __load_users(data: dict) -> None:
        """Передача информации о пользователях в БД"""

        for key, content in data.items():
            user, created = CustomUser.objects.get_or_create(**content)
            if created:
                print(f"Добавлен новый пользователь с уникальным адресом электронной почты <{key}>.")
            else:
                print(f"Пользователь с уникальным адресом электронной почты <{key}> уже существует в базе данных.")

    @staticmethod
    def __set_group_permissions(group: Group, data: list) -> None:
        """Устанавливает разрешения группе пользователей"""

        for i in data:
            content_type = ContentType.objects.get_or_create(app_label=i.get("app_label"), model=i.get("model"))[0]
            permission_name = i.get("codename").replace("_", " ")
            permission, created = Permission.objects.get_or_create(
                content_type=content_type, codename=i.get("codename"), defaults={"name": permission_name}
            )
            if created:
                print(f"Создано новое разрешение <{permission_name}>.")
            group.permissions.add(permission)
            print(f"Группа <{group.name}> получила разрешение <{permission_name}>.")

    @staticmethod
    def __set_group_users(group: Group, data: list) -> None:
        """Определяет принадлежность пользователей к группам"""

        for i in data:
            user = CustomUser.objects.get(email=i)
            user.groups.add(group)
            print(f"Пользователь с уникальным адресом электронной почты <{i}> был добавлен в группу <{group.name}>.")

    def __load_groups(self, data: dict) -> None:
        """Запись в БД данных о группах пользователей и их разрешениях"""

        for name, content in data.items():
            group, created = Group.objects.get_or_create(name=name)
            if created:
                print(f"\nСоздана новая группа пользователей <{name}>.")
            else:
                print(
                    f"\nГруппа <{name}> уже существует в базе данных. Возможно, "
                    + "в нее будут добавлены новые пользователи, а также может измениться список ее разрешений."
                )
            self.__set_group_permissions(group, content["permissions"])
            self.__set_group_users(group, content.get("users", list()))

    def handle(self, *args: Any, **options: Any) -> None:
        """Вызов команды из терминала"""

        data = self.__get_data()
        self.__load_users(data.get("users", dict()))
        self.__load_groups(data.get("groups", dict()))
