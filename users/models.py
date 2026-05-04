from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя проекта Sky Store"""

    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Адрес электронной почты")
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True, verbose_name="Фото")
    phone_number: models.CharField = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    country: models.CharField = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")

    class Meta:
        """Класс представления пользователя в админ-панели"""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        """Метод строкового представления пользователя"""

        return f"{self.username}: {self.email}"
