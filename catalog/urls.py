from django.urls import path

from . import views
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("catalog/page/<int:page>/", views.HomeListView.as_view(), name="catalog"),
    path("contacts/", views.ContactCreateView.as_view(), name="contacts"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product"),
    path("select_category/", views.SelectCategoryListView.as_view(), name="select_category"),
    path("create_category/", views.CategoryCreateView.as_view(), name="create_category"),
    path("create_product/<int:cat_id>/", views.CreateProductCreateView.as_view(), name="create_product"),
]
