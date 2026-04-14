from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Category, Contact, Product


def home(request: HttpRequest, page_number: int = 1) -> HttpResponse:
    """Контроллер главной страницы Каталог"""

    products = Product.objects.all().order_by("-created_at")
    context = None
    if len(products) > 0:
        paged_products = [products[i : i + 8] for i in range(0, len(products), 8)]
        context = {
            "products": paged_products[page_number - 1],
            "pages_count": [i + 1 for i in range(len(paged_products))],
        }
    return render(request, "home.html", context=context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы Контакты"""

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        Contact.objects.get_or_create(name=name, phone=phone, message=message)
        return render(request, "successful_sending.html")
    return render(request, "contacts.html")


def product(request: HttpRequest, pk: int) -> HttpResponse:
    """Контроллер страницы определенного продукта"""

    return render(request, "product.html", context={"product": Product.objects.get(id=pk)})


def select_category(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы выбора категории размещаемого товара"""

    categories = Category.objects.all()
    context = None
    if len(categories) > 0:
        context = {"categories": Category.objects.all()}
    return render(request, "select_category.html", context=context)


def create_product(request: HttpRequest, cat_id: int) -> HttpResponse:
    """Контроллер страницы размещения новых продуктов"""

    current_category = Category.objects.get(id=cat_id)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        path_to_photo = None
        if request.POST.get("photo"):
            file = request.FILES["photo"]
            if isinstance(file, UploadedFile):
                default_storage.save(f"images/{file.name}", ContentFile(file.read()))
                path_to_photo = f"images/{file.name}"
        price = request.POST.get("price")
        Product.objects.create(
            name=name, description=description, photo=path_to_photo, price=price, category=current_category
        )
        return render(request, "successful_sending.html")
    return render(request, "create_product.html", context={"category": current_category})


def create_category(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы создания новой категории продуктов"""

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        Category.objects.create(name=name, description=description)
        return redirect("/select_category/")
    return render(request, "create_category.html")
