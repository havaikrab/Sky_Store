from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Product

FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


def validate_forbidden_words(value: str) -> None:
    """Функция-валидатор, исключающая использование слов из списка FORBIDDEN_WORDS"""

    for word in FORBIDDEN_WORDS:
        if word in value.lower():
            raise ValidationError(f"Запрещено использовать слово {word}!")


class CategoryForm(forms.ModelForm):
    """Форма для создания нового продукта"""

    class Meta:
        """Класс содержания формы"""

        model = Category
        fields = ["name", "description"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение родительского метода, для стилизации формы"""

        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Опишите категорию"})


class ProductForm(forms.ModelForm):
    """Форма для создания нового продукта"""

    class Meta:
        """Класс содержания формы"""

        model = Product
        fields = ["name", "description", "price", "category"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение родительского метода, для стилизации формы"""

        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control errors_list", "placeholder": "Введите название"}
        )
        self.fields["name"].validators.append(validate_forbidden_words)
        self.fields["description"].widget.attrs.update(
            {"class": "form-control errors_list", "placeholder": "Опишите продукт"}
        )
        self.fields["description"].validators.append(validate_forbidden_words)
        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите цену в рублях"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})

    def clean_price(self) -> int:
        """Валидатор поля price"""

        price = self.cleaned_data.get("price")
        if isinstance(price, int):
            if price <= 0:
                raise ValidationError("Цена не может быть меньше или равна нулю")
            return price
        raise ValidationError("Цена должна быть числом")
