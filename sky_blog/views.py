from django.views.generic import DetailView, ListView

from .models import Article


class BlogHome(ListView):
    """Контроллер главной страницы приложения Sky Blog"""

    model = Article
    paginate_by = 8


class ArticleDetailView(DetailView):
    """Контроллер страницы статьи блога"""

    model = Article
