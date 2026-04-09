from django.urls import path

from . import views
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("product/<int:pk>/", views.product, name="product"),
    path("select_category/", views.select_category, name="select_category"),
    path("create_category/", views.create_category, name="create_category"),
    path("create_product/<int:cat_id>/", views.create_product, name="create_product"),
]
