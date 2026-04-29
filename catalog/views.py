from typing import Any

from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoryForm, ProductForm
from .models import Category, Contact, Product


def valid_photo(photo: Any, form: BaseModelForm) -> bool:
    """Метод валидации загружаемого файла в поле фото"""

    valid_extensions = ["jpeg", "png"]
    file_extension = photo.name.split(".")[-1].lower()
    if file_extension not in valid_extensions:
        form.add_error(None, f"Допустимые расширения jpeg или png, расширение {file_extension} не поддерживается")
        return False
    if photo.size > 5 * 2**20:
        form.add_error(
            None, f"Размер загружаемого файла не должен превышать 5 MB, ваш файл весит {int(photo.size / 2 ** 20)} MB."
        )
        return False
    return True


class HomeListView(ListView):
    """Контроллер главной страницы приложения Каталог"""

    model = Product
    paginate_by = 8
    ordering = ["-created_at"]


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

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Переопределение родительского метода, включающее в форму описанное в шаблоне поле photo"""

        uploaded_photo = self.request.FILES.get("photo")
        if uploaded_photo is None:
            return super().form_valid(form)
        elif valid_photo(uploaded_photo, form):
            form.instance.photo = uploaded_photo
            return super().form_valid(form)
        return self.form_invalid(form)


class ProductDetailView(DetailView):
    """Контроллер отображения страницы определенного продукта"""

    model = Product


class ProductUpdateView(UpdateView):
    """Контроллер страницы редактирования информации о продукте"""

    model = Product
    form_class = ProductForm

    def get_success_url(self) -> Any:
        """Метод получения url после редактирования информации о продукте"""

        return reverse_lazy("catalog:product", kwargs={"pk": self.object.pk})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Добавление возможности обновить поле photo или удалить его содержимое из БД"""

        delete_photo = self.request.POST.get("delete_photo")
        if delete_photo == "true":
            self.object.photo.delete(save=False)
            self.object.photo = None
        new_photo = self.request.FILES.get("photo")
        if new_photo is None:
            return super().form_valid(form)
        elif valid_photo(new_photo, form):
            self.object.photo = new_photo
            return super().form_valid(form)
        return self.form_invalid(form)


class ProductDeleteView(DeleteView):
    """Контроллер удаления продукта"""

    model = Product
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Метод, проверяющий необходимость удалить существующее в фото продукта"""

        if self.object.photo is not None:
            self.object.photo.delete(save=False)
        return super().form_valid(form)


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
