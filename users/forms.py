from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    class Meta(UserCreationForm.Meta):
        """Класс содержания формы"""

        model = CustomUser
        fields = ['username', 'email', 'avatar', 'phone_number', 'country']

