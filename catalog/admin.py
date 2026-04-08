from django.contrib import admin

from .models import Category, Contact, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс описания модели Category в админ-панели"""

    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс описания модели Product в админ-панели"""

    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Класс описания модели Contact в админ-панели"""

    list_display = ("name", "phone")
