from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.models import CustomUser

from .models import Article


class BlogHome(ListView):
    """Контроллер главной страницы приложения Sky Blog"""

    model = Article
    paginate_by = 8
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet:
        """Контроль отображения только опубликованных статей"""

        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs: Any) -> dict:
        """Передача заголовка в шаблон"""

        context = super().get_context_data(**kwargs)
        context.update({"title": "Sky Blog", "greeting": True, "page_url_name": "sky_blog:blog"})
        return context


class BlogUnpublishedList(PermissionRequiredMixin, ListView):
    """Контроллер страницы неопубликованных статей"""

    model = Article
    paginate_by = 8
    ordering = ["created_at"]
    permission_required = ("sky_blog.change_article", "sky_blog.delete_article")

    def get_queryset(self) -> QuerySet:
        """Отбор неопубликованных статей для отображения"""

        return super().get_queryset().filter(is_published=False)

    def get_context_data(self, **kwargs: Any) -> dict:
        """Передача заголовка в шаблон"""

        context = super().get_context_data(**kwargs)
        context.update({"title": "Article moderation", "page_url_name": "sky_blog:unpublished"})
        return context


class ArticleDetailView(DetailView):
    """Контроллер страницы статьи блога"""

    model = Article

    def get_object(self, queryset: Optional[QuerySet] = None) -> Article:
        """Ограничение доступа к неопубликованным статьям пользователей,
        не зарегистрированных в группе контент-менеджеров,
        увеличение счетчика просмотров статьи при посещении ее страницы пользователем"""

        article = super().get_object(queryset)
        current_user = self.request.user
        if isinstance(article, Article) and isinstance(current_user, CustomUser):
            if not article.is_published and not current_user.has_perms(
                ["sky_blog.change_article", "sky_blog.delete_article"]
            ):
                raise PermissionDenied
            article.views_count += 1
            article.save()
            if article.views_count == 100 and isinstance(EMAIL_HOST_USER, str):
                try:
                    send_mail(
                        "Поздравляем!",
                        f'Статья "{article.title}" была прочитана 100 раз',
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[EMAIL_HOST_USER],
                        fail_silently=False,
                    )
                    print("Поздравление было успешно отправлено")
                except TimeoutError:
                    print("Попытка установить соединение была безуспешной.")
            return article
        raise PermissionDenied


class CreateArticle(LoginRequiredMixin, CreateView):
    """Контроллер страницы написания новой статьи"""

    model = Article
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("sky_blog:blog", kwargs={"page": 1})


class UpdateArticle(PermissionRequiredMixin, UpdateView):
    """Контроллер страницы редактирования существующей статьи"""

    model = Article
    fields = ("title", "content", "preview", "is_published")
    permission_required = ("sky_blog.change_article", "sky_blog.delete_article")

    def get_success_url(self) -> Any:
        """Метод получения url статьи для перехода после ее редактирования"""

        return reverse_lazy("sky_blog:article", kwargs={"pk": self.object.pk})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, проверяющий необходимость удалить существующее в статье изображение"""

        delete_preview = self.request.POST.get("delete_image")
        if delete_preview is True:
            self.object.preview.delete(save=False)
            self.object.preview = None
        return super().form_valid(form)


class DeleteArticle(PermissionRequiredMixin, DeleteView):
    """Контроллер удаления статьи"""

    model = Article
    success_url = reverse_lazy("sky_blog:blog", kwargs={"page": 1})
    permission_required = ("sky_blog.change_article", "sky_blog.delete_article")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, проверяющий необходимость удалить существующее в статье изображение"""

        if self.object.preview is not None:
            self.object.preview.delete(save=False)
        return super().form_valid(form)
