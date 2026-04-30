from django.contrib.auth import login
from django.core.mail import send_mail
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from support_funcs.validators import common_file_validator

from .forms import CustomUserCreationForm


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
