from typing import Any

from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .models import Category, Contact, Product


class HomeListView(ListView):
    """Контроллер главной страницы приложения Каталог"""

    model = Product
    paginate_by = 8
    ordering = ["-created_at"]


class ProductDetailView(DetailView):
    """Контроллер отображения страницы определенного продукта"""

    model = Product


class SelectCategoryListView(ListView):
    """Контроллер страницы выбора категории размещаемого продукта"""

    model = Category


class CategoryCreateView(CreateView):
    """Контроллер страницы создания новой категории продуктов"""

    model = Category
    fields = ("name", "description")
    success_url = reverse_lazy("catalog:select_category")


class CreateProductCreateView(CreateView):
    """Контроллер страницы создания нового продукта"""

    model = Product
    fields = ("name", "description", "photo", "price")
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, устанавливающий значение поля Category, переданное в url"""

        category_id = self.kwargs.get("cat_id")
        form.instance.category_id = category_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод, добавляющий в контекст шаблона информацию о категории создаваемого продукта"""

        category_id = self.kwargs.get("cat_id")
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=category_id)
        return context


class ContactCreateView(CreateView):
    """Контроллер страницы Контакты"""

    model = Contact
    fields = ("name", "phone", "message")
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, сообщающий об успешном сохранении контактов пользователя в БД"""

        print(type(form))
        response = super().form_valid(form)
        messages.success(self.request, "Ваша контактная информация сохранена")
        return response
