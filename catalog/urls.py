from django.urls import path
from . apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
path('contacts/', views.contacts, name='contacts'),
]
