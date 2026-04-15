from django.urls import path

from . import views
from .apps import SkyBlogConfig

app_name = SkyBlogConfig.name

urlpatterns = [
    path("blog/page/<int:page>/", views.BlogHome.as_view(), name="blog"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article"),
]
