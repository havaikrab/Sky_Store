from django.urls import path

from . import views
from .apps import SkyBlogConfig


app_name = SkyBlogConfig.name

urlpatterns = [
    path("blog/page/<int:page>/", views.BlogHome.as_view(), name="blog"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article"),
    path("create_article/", views.CreateArticle.as_view(), name="create_article"),
    path("article/update/<int:pk>/", views.UpdateArticle.as_view(), name="update_article"),
    path("article/delete/<int:pk>/", views.DeleteArticle.as_view(), name="delete_article"),
]
