from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Контроллер регистрации нового пользователя"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")
    template_name = "users/register.html"
