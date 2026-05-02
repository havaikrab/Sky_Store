from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.forms import ModelForm, PasswordInput
from django.urls import reverse

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    class Meta(UserCreationForm.Meta):
        """Класс содержания формы"""

        model = CustomUser
        fields = ("username", "email", "avatar", "phone_number", "country")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение стилизации формы с помощью библиотеки crispy-forms"""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        button = Submit("submit", "Зарегистрироваться")
        button.field_classes = "p-2 btn btn-outline-primary"
        self.helper.layout = Layout(
            "username", "email", "avatar", "phone_number", "country", "password1", "password2", button
        )


class CustomUserUpdateForm(UserChangeForm):
    """Форма редактирования личных данных пользователя"""

    class Meta(UserChangeForm.Meta):
        """Класс содержания формы"""

        model = CustomUser
        fields = ("username", "email", "avatar", "phone_number", "country")  # type: ignore

    def __init__(self, *args: Any, **kwargs: Any):

        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        save_button = Submit("submit", "Сохранить")
        save_button.field_classes = "p-2 btn btn-outline-primary me-2"
        password_url = reverse("users:change_password")
        password_button = HTML(f'<a href="{password_url}" class="p-2 btn btn-outline-primary me-2">Сменить пароль</a>')
        delete_url = reverse("users:delete_profile")
        delete_button = HTML(f'<a href="{delete_url}" class="p-2 btn btn-outline-danger mt-3">Удалить профиль</a>')
        self.helper.layout = Layout(
            "username", "email", "avatar", "phone_number", "country", Div(save_button, password_button), delete_button
        )


class CustomUserPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароль пользователя"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Добавление в стандартную форму кнопки Подтверждения"""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        submit_button = Submit("submit", "Подтвердить")
        submit_button.field_classes = "p-2 btn btn-outline-primary"
        cancel_url = reverse("users:update_profile")
        cancel_button = HTML(f'<a href="{cancel_url}" class="p-2 btn btn-outline-primary">Отмена</a>')
        self.helper.layout = Layout("old_password", "new_password1", "new_password2", submit_button, cancel_button)


class CustomUserDeleteForm(ModelForm):
    """Форма с паролем для подтверждения удаления аккаунта пользователя"""

    class Meta:
        """Описание содержимого формы"""

        model = CustomUser
        fields = ["password"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение родительского метода, для стилизации формы"""

        super(CustomUserDeleteForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = PasswordInput(attrs={"class": "form-control"})
