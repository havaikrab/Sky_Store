from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Article


class BlogHome(ListView):
    """Контроллер главной страницы приложения Sky Blog"""

    model = Article
    paginate_by = 8
    ordering = ["-created_at"]


class ArticleDetailView(DetailView):
    """Контроллер страницы статьи блога"""

    model = Article


class CreateArticle(CreateView):
    """Контроллер страницы написания новой статьи"""

    model = Article
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("sky_blog:blog", kwargs={"page": 1})


class UpdateArticle(UpdateView):
    """Контроллер страницы редактирования существующей статьи"""

    model = Article
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("sky_blog:blog", kwargs={"page": 1})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, проверяющий необходимость удалить существующее в статье изображение"""

        delete_preview = self.request.POST.get("delete_image")
        if delete_preview is not None:
            self.object.preview.delete(save=False)
            self.object.preview = None
        return super().form_valid(form)


class DeleteArticle(DeleteView):
    """Контроллер удаления статьи"""

    model = Article
    success_url = reverse_lazy("sky_blog:blog", kwargs={"page": 1})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, проверяющий необходимость удалить существующее в статье изображение"""

        if self.object.preview is not None:
            self.object.preview.delete(save=False)
            self.object.preview = None
        return super().form_valid(form)
