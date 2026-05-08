from typing import Any, Optional

from django.contrib import messages as msgs
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from support_funcs.validators import common_file_validator

from .forms import CustomUserCreationForm, CustomUserDeleteForm, CustomUserPasswordChangeForm, CustomUserUpdateForm
from .models import CustomUser


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения профиля пользователя"""

    model = CustomUser
    template_name = "users/profile.html"

    def get_object(self, queryset: Optional[QuerySet] = None) -> AbstractBaseUser | AnonymousUser:
        """Определение объекта зарегистрированного пользователя"""

        return self.request.user


class RegisterView(CreateView):
    """Контроллер регистрации нового пользователя"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")
    template_name = "users/register.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Добавление валидации загружаемого фото и функции отправки письма пользователю при успешной регистрации"""

        uploaded_photo = self.request.FILES.get("avatar")
        if uploaded_photo is None or common_file_validator(
            file=uploaded_photo, form=form, valid_extensions=["jpeg", "png", "jpg"], size_limit=5, field_name="avatar"
        ):
            response = super().form_valid(form)
            login(self.request, self.object)
            if self.object is not None:
                try:
                    send_mail(
                        "Поздравляем! Вы зарегистрировались в Sky Store!",
                        f"""Ваше имя пользователя в Sky Store: {self.object.username}""",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[self.object.email],
                        fail_silently=False,
                    )
                    print("Сообщение было успешно отправлено")
                except TimeoutError:
                    print("Попытка установить соединение была безуспешной.")
                return response
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "users/update_profile.html"
    success_url = reverse_lazy("users:profile")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Добавление поля для последующего возможного сохранения в нем пути к текущему фото пользователя"""
        super().__init__(*args, **kwargs)
        self.old_photo: ImageFieldFile | None = None

    def get_object(self, queryset: Optional[QuerySet] = None) -> AbstractBaseUser | AnonymousUser:
        """Определение объекта авторизованного пользователя и заполнение поля old_photo"""

        current_user = self.request.user
        if isinstance(current_user, CustomUser):
            self.old_photo = current_user.avatar
        return current_user

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Проверка наличия в форме отметки об удалении старого фото пользователя"""

        new_photo = form.cleaned_data.get("avatar")
        clear_photo = self.request.POST.get("avatar-clear")
        response = super().form_valid(form)
        if self.old_photo:
            if clear_photo == "on" or new_photo:
                self.old_photo.delete(save=False)
        return response


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Контроллер страницы смены пароля пользователя"""

    template_name = "users/update_profile.html"
    form_class = CustomUserPasswordChangeForm
    success_url = reverse_lazy("users:update_profile")

    def form_valid(self, form: PasswordChangeForm) -> HttpResponse:
        """Добавление сообщения об успешной смене пароля"""

        msgs.success(self.request, "Новый пароль был успешно сохранен.", extra_tags="S_P_CH")

        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления аккаунта пользователя"""

    model = CustomUser
    form_class = CustomUserDeleteForm
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset: Optional[QuerySet] = None) -> AbstractBaseUser | AnonymousUser:
        """Определение объекта удаляемого пользователя"""

        return self.request.user

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Проверка пароля перед удалением аккаунта"""

        password = form.cleaned_data.get("password")
        if self.request.user.check_password(password):
            if self.object.avatar:
                self.object.avatar.delete(save=False)
            return super().form_valid(form)
        else:
            form.add_error("password", "Неверный пароль")
            return super().form_invalid(form)
