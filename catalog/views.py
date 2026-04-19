from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CategoryForm, ProductForm
from .models import Category, Contact, Product


class HomeListView(ListView):
    """Контроллер главной страницы приложения Каталог"""

    model = Product
    paginate_by = 8
    ordering = ["-created_at"]


class ProductDetailView(DetailView):
    """Контроллер отображения страницы определенного продукта"""

    model = Product


class CategoryListView(ListView):
    """Контроллер страницы выбора категории размещаемого продукта"""

    model = Category


class CategoryCreateView(CreateView):
    """Контроллер страницы создания новой категории продуктов"""

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:select_category")


class ProductCreateView(CreateView):
    """Контроллер страницы создания нового продукта"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_initial(self) -> dict:
        """Метод, предопределяющий значение категории продукта"""

        initial = super().get_initial()
        category_id = self.kwargs.get("cat_id")
        if category_id:
            current_category = Category.objects.get(id=category_id)
            initial["category"] = current_category
        return initial


class ContactCreateView(CreateView):
    """Контроллер страницы Контакты"""

    model = Contact
    fields = ("name", "phone", "message")
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, сообщающий об успешном сохранении контактов пользователя в БД"""

        response = super().form_valid(form)
        messages.success(self.request, "Ваша контактная информация сохранена")
        return response
