from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm

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
        self.fields["username"].label = "Имя пользователя"
        self.fields["username"].help_text = "Не более 150 символов"
        self.fields["password1"].label = "Пароль"
        self.fields["password1"].help_text = """
<ul>
<li>Ваш пароль не должен быть слишком похож на другие ваши персональные данные.</li>
<li>Ваш пароль должен содержать не менее 8 символов.</li>
<li>Ваш пароль не может быть очень простым.</li>
<li>Ваш пароль не может полностью состоять из цифр.</li>
</ul>
"""
        self.fields["password2"].label = "Подтвердите пароль"
        self.fields["password2"].help_text = "Введите пароль повторно"
