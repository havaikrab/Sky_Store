from typing import Any

from django import forms

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
        fields = ["name", "description", "price", "photo", "category"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение родительского метода, для стилизации формы"""

        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Опишите продукт"})
        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите цену в рублях"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["photo"].widget.attrs.update({"class": "form-control"})
