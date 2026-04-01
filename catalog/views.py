from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Контроллер главной страницы Каталог"""

    return render(request, "home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы Контакты"""

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print({"name": name, "phone": phone, "message": message})
        return render(request, "successful_sending.html")
    return render(request, "contacts.html")
