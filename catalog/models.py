from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Класс описания категории продуктов"""

    name: models.CharField = models.CharField(
        max_length=100,
        verbose_name="Название",
    )
    description: models.TextField = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self) -> str:
        """Метод строкового представления информации о категории продуктов"""

        return str(self.name)

    class Meta:
        """Класс представления категории продуктов в админ-панели Django"""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    """Класс описания продукта"""

    name: models.CharField = models.CharField(max_length=100, verbose_name="Название")
    description: models.TextField = models.TextField(verbose_name="Описание", blank=True, null=True)
    photo: models.ImageField = models.ImageField(upload_to="images", verbose_name="Фото", blank=True, null=True)
    category: models.ForeignKey = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория"
    )
    price: models.IntegerField = models.IntegerField(verbose_name="Цена")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published: models.BooleanField = models.BooleanField(verbose_name="Статус публикации", default=False)
    owner: models.ForeignKey = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="products", verbose_name="Владелец", default=20
    )

    def __str__(self) -> str:
        """Метод строкового представления информации о продукте"""

        return str(self.name)

    class Meta:
        """Класс представления продукта в админ-панели Django"""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "price"]
        permissions = [("can_unpublish_product", "Может отменять публикацию продукта")]


class Contact(models.Model):
    """Класс описания контактов пользователя"""

    name: models.CharField = models.CharField(max_length=100, verbose_name="Имя")
    phone: models.CharField = models.CharField(max_length=100, verbose_name="Телефон")
    message: models.TextField = models.TextField(verbose_name="Сообщение", blank=True, null=True)

    def __str__(self) -> str:
        """Метод строкового представления информации о контактах пользователя"""

        return f"{self.name}: {self.phone}"

    class Meta:
        """Класс представления контактов пользователя в админ-панели Django"""

        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["name"]
