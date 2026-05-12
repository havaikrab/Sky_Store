from django.urls import path

from . import views
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("moderator_control/<int:page>/", views.ModerationRequiredListView.as_view(), name="moderator_control"),
    path("catalog/<int:page>/", views.HomeListView.as_view(), name="catalog"),
    path(
        "products_by_category/<int:cat_id>/", views.ProductsByCategoryListView.as_view(), name="products_by_category"
    ),
    path("contacts/", views.ContactCreateView.as_view(), name="contacts"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product"),
    path("product/update/<int:pk>/", views.ProductUpdateView.as_view(), name="update_product"),
    path("product/delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("select_category/", views.CategoryListView.as_view(), name="select_category"),
    path("create_category/", views.CategoryCreateView.as_view(), name="create_category"),
    path("create_product/", views.ProductCreateView.as_view(), name="create_product_no_category"),
    path("create_product/<int:cat_id>/", views.ProductCreateView.as_view(), name="create_product"),
    path("publish_product/<int:pk>/", views.ProductPublishView.as_view(), name="publish_product"),
    path("reject_product/<int:pk>/", views.ProductRejectView.as_view(), name="reject_product"),
]
