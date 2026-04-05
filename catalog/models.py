from django.db import models


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

    def __str__(self) -> str:
        """Метод строкового представления информации о продукте"""

        return str(self.name)

    class Meta:
        """Класс представления продукта в админ-панели Django"""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "price"]
