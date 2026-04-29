from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register')
]