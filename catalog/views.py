from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    """Контроллер главной страницы Каталог"""

    fresh_products = list(Product.objects.all().order_by("created_at"))[-5:]
    for product in fresh_products:
        print(product)
    context = {"fresh_products": fresh_products}
    return render(request, "home.html", context=context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы Контакты"""

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        new_contact = Contact.objects.get_or_create(name=name, phone=phone, message=message)
        print(new_contact[0])
        return render(request, "successful_sending.html")
    return render(request, "contacts.html")
