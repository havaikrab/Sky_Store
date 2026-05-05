from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError

from support_funcs.validators import validate_forbidden_words

from .models import Category, Product


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
        fields = ["name", "description", "price", "category", "photo"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение родительского метода, для стилизации формы"""

        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["name"].validators.append(validate_forbidden_words)
        self.fields["name"].error_messages = {
            "required": "Пожалуйста, введите название продукта.",
            "max_length": "Слишком длинное название. Используйте не более 1133 символов.",
            "unique": "Продукт с таким названием уже существует",
        }
        self.fields["description"].validators.append(validate_forbidden_words)
        button = Submit("submit", "Сохранить")
        button.field_classes = "p-2 btn btn-outline-primary"
        self.helper.layout = Layout(
            Field(
                "name",
                placeholder="Введите название",
                css_class="errors_list",
            ),
            Field("description", placeholder="Опишите продукт", css_class="errors_list"),
            Field("price", placeholder="Укажите цену в рублях"),
            "category",
            "photo",
            button,
        )

    def clean_price(self) -> int:
        """Валидатор поля price"""

        price = self.cleaned_data.get("price")
        if isinstance(price, int):
            if price <= 0:
                raise ValidationError("Цена не может быть меньше или равна нулю")
            return price
        raise ValidationError("Цена должна быть числом")
