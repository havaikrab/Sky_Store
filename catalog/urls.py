from django.urls import path

from . import views
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("moderator_control/", views.ModerationRequiredListView.as_view(), name="moderator_control"),
    path("catalog/page/<int:page>/", views.HomeListView.as_view(), name="catalog"),
    path("contacts/", views.ContactCreateView.as_view(), name="contacts"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product"),
    path("product/update/<int:pk>/", views.ProductUpdateView.as_view(), name="update_product"),
    path("product/delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("select_category/", views.CategoryListView.as_view(), name="select_category"),
    path("create_category/", views.CategoryCreateView.as_view(), name="create_category"),
    path("create_product/", views.ProductCreateView.as_view(), name="create_product_no_category"),
    path("create_product/<int:cat_id>/", views.ProductCreateView.as_view(), name="create_product"),
]
