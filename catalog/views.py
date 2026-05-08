from typing import Any, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from support_funcs.validators import common_file_validator
from users.models import CustomUser

from .forms import CategoryForm, ProductForm
from .models import Category, Contact, Product


class HomeListView(ListView):
    """Контроллер главной страницы приложения Каталог"""

    model = Product
    paginate_by = 8
    ordering = ["-updated_at"]

    def get_queryset(self) -> QuerySet:
        """Определение списка продуктов, разрешенных для публикации"""

        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs: Any) -> dict:
        """Передача заголовка в шаблон"""

        context = super().get_context_data(**kwargs)
        context.update({"title": "Каталог Sky Store", "greeting": True, "page_url_name": "catalog:catalog"})
        return context


class ModerationRequiredListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер страницы, продуктов требующих проверки модератором"""

    model = Product
    permission_required = ("catalog.delete_product", "catalog.can_unpublish_product")
    paginate_by = 8
    ordering = ["updated_at"]

    def get_queryset(self) -> QuerySet:
        """Определение списка продуктов, разрешенных для публикации"""

        return super().get_queryset().filter(is_published=False)

    def get_context_data(self, **kwargs: Any) -> dict:
        """Передача заголовка в шаблон"""

        context = super().get_context_data(**kwargs)
        context.update({"title": "Product moderation", "page_url_name": "catalog:moderator_control"})
        return context


class CategoryListView(ListView):
    """Контроллер страницы выбора категории размещаемого продукта"""

    model = Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы создания новой категории продуктов"""

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:select_category")


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы создания нового продукта"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_initial(self) -> dict:
        """Метод, предопределяющий значение категории продукта"""

        initial = super().get_initial()
        category_id = self.kwargs.get("cat_id")
        if category_id:
            initial["category"] = Category.objects.get(id=category_id)
        return initial

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Указание авторизованного пользователя в качестве владельца продукта
        и добавление валидации загружаемого файла в поле photo"""

        form.instance.owner = self.request.user
        uploaded_photo = self.request.FILES.get("photo")
        if uploaded_photo is None:
            messages.success(
                self.request, "Ваш продукт станет доступным в каталоге Sky Store после проверки модератором"
            )
            return super().form_valid(form)
        elif common_file_validator(
            file=uploaded_photo, form=form, valid_extensions=["jpeg", "png"], size_limit=5, field_name="photo"
        ):
            form.instance.photo = uploaded_photo
            messages.success(
                self.request, "Ваш продукт станет доступным в каталоге Sky Store после проверки модератором"
            )
            return super().form_valid(form)
        return self.form_invalid(form)


class ProductDetailView(DetailView):
    """Контроллер отображения страницы определенного продукта"""

    model = Product

    def get_object(self, queryset: Optional[QuerySet] = None) -> Product:
        """Ограничение доступа к страницам неопубликованных продуктов пользователей,
        не зарегистрированных в группе модераторов"""

        current_product = super().get_object()
        current_user = self.request.user
        if isinstance(current_product, Product) and isinstance(current_user, CustomUser):
            if not current_product.is_published and not current_user.has_perms(
                ["catalog.delete_product", "catalog.can_unpublish_product"]
            ):
                raise PermissionDenied
            return current_product
        raise PermissionDenied

    def get_context_data(self, **kwargs: Any) -> dict:
        """Передача в шаблон статуса пользователя"""

        context = super().get_context_data(**kwargs)
        if isinstance(self.request.user, CustomUser):
            if self.request.user.pk == self.object.owner_id:
                context.update({"owner": True})
            if self.request.user.has_perms(["catalog.delete_product", "catalog.can_unpublish_product"]):
                context.update({"moderator": True})
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер страницы редактирования информации о продукте"""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Добавление поля для последующего возможного сохранения в нем пути к текущему фото продукта"""
        super().__init__(*args, **kwargs)
        self.old_photo: ImageFieldFile | None = None

    def get_object(self, queryset: Optional[QuerySet] = None) -> Product:
        """Определение объекта продукта, предоставление доступа к редактированию продукта только его владельцу
        и заполнение поля old_photo"""

        current_object = super().get_object()
        if isinstance(current_object, Product):
            if current_object.owner == self.request.user:
                self.old_photo = current_object.photo
                return current_object
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Удаление старой фотографии продукта при изменении данных в поле photo"""

        new_photo = form.cleaned_data.get("photo")
        clear_photo = self.request.POST.get("photo-clear")
        self.object.is_published = False
        response = super().form_valid(form)
        if self.old_photo:
            if clear_photo == "on" or new_photo:
                self.old_photo.delete(save=False)
        messages.success(
            self.request,
            """Ваш измененный продукт ожидает проверки модератором, скоро он станет доступным в каталоге Sky Store""",
        )
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления продукта"""

    model = Product
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset: Optional[QuerySet] = None) -> Product:
        """Проверка прав пользователя на удаление продукта"""

        current_object = super().get_object()
        if isinstance(current_object, Product) and isinstance(self.request.user, CustomUser):
            if self.request.user.has_perm("catalog.delete_product") or current_object.owner == self.request.user:
                return current_object
        raise PermissionDenied

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


class ProductPublishView(PermissionRequiredMixin, RedirectView):
    """Контроллер подтверждения статуса публикации продукта"""

    permanent = False
    permission_required = "catalog.can_unpublish_product"

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        """Изменение статуса публикации продукта без рендеринга отдельной страницы
        и редирект на страницу каталога опубликованных продуктов"""

        product_id = kwargs.get("pk")
        current_product = Product.objects.get(id=product_id)
        if isinstance(current_product, Product):
            current_product.is_published = True
            current_product.save()
        return reverse("catalog:home")


class ProductRejectView(RedirectView):
    """Контроллер подтверждения статуса публикации продукта"""

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        """Изменение статуса публикации продукта без рендеринга отдельной страницы
        и редирект на страницу каталога опубликованных продуктов"""

        product_id = kwargs.get("pk")
        product = Product.objects.get(id=product_id)
        current_user = self.request.user
        if isinstance(product, Product) and isinstance(current_user, CustomUser):
            if current_user.has_perm("catalog.can_unpublish_product") or current_user == product.owner:
                product.is_published = False
                product.save()
                return reverse("catalog:home")
        raise PermissionDenied
