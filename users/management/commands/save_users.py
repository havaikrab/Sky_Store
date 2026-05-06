import json
from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Сохраняет текущее состояние базы данных для приложения users"

    @staticmethod
    def __save_groups() -> dict:
        """Получение всех существующих в БД групп со списками их пользователей и разрешений"""

        groups_dict = dict()
        for group in Group.objects.all():
            groups_dict.update(
                {
                    group.name: {
                        "permissions": [
                            {
                                "app_label": permission.content_type.app_label,
                                "model": permission.content_type.model,
                                "codename": permission.codename,
                            }
                            for permission in group.permissions.all()
                        ],
                        "users": [user.email for user in group.user_set.all()],  # type: ignore
                    }
                }
            )
        return groups_dict

    @staticmethod
    def __save_users() -> dict:
        """Получение всех существующих в БД пользователей"""

        users_dict = dict()
        for user in CustomUser.objects.all():
            users_dict.update(
                {
                    user.email: {
                        "username": user.username,
                        "email": user.email,
                        "avatar": user.avatar.name,
                        "phone_number": user.phone_number,
                        "country": user.country,
                        "password": user.password,
                        "is_superuser": user.is_superuser,
                        "is_staff": user.is_staff,
                        "is_active": user.is_active,
                    }
                }
            )
        return users_dict

    def handle(self, *args: Any, **options: Any) -> None:
        """Запись данных приложения users в файл fixture/fixture_users.json"""

        data: dict = dict()
        data["groups"] = self.__save_groups()
        data["users"] = self.__save_users()
        with open("fixture/fixture_users.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
