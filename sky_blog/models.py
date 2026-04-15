from django.db import models


class Article(models.Model):
    """Модель описания статьи блога"""

    title: models.CharField = models.CharField(max_length=100, verbose_name="Заголовок")
    content: models.TextField = models.TextField(verbose_name="Содержимое")
    preview: models.ImageField = models.ImageField(upload_to="images", verbose_name="Превью", blank=True, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published: models.BooleanField = models.BooleanField(verbose_name="Признак публикации")
    views_count: models.IntegerField = models.IntegerField(verbose_name="Количество просмотров", default=0)

    def __str__(self) -> str:
        """Метод строкового представления информации о статье блога"""

        return str(self.title)

    class Meta:
        """Класс представления статьи в админ-панели Django"""

        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title"]
