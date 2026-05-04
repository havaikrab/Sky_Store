from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .apps import UsersConfig
from .views import ProfileDeleteView, ProfileDetailView, ProfileUpdateView, RegisterView, UserPasswordChangeView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="catalog:home"), name="logout"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("edit_profile/", ProfileUpdateView.as_view(), name="update_profile"),
    path("change_password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("delete/", ProfileDeleteView.as_view(), name="delete_profile"),
]
