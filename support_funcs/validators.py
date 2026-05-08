from typing import Optional

from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.forms import BaseModelForm

FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


def validate_forbidden_words(value: str) -> None:
    """Функция-валидатор, исключающая использование слов из списка FORBIDDEN_WORDS"""

    for word in FORBIDDEN_WORDS:
        if word in value.lower():
            raise ValidationError(f"Запрещено использовать слово {word}!")


def common_file_validator(
    file: File, form: BaseModelForm, valid_extensions: list, size_limit: int, field_name: Optional[str] = None
) -> bool:
    """Метод валидации файла по расширению и размеру"""

    if isinstance(file.name, str):
        file_extension = file.name.split(".")[-1].lower()
        if file_extension not in valid_extensions:
            form.add_error(
                field_name,
                f"Допустимые расширения {", ".join(valid_extensions)}, расширение {file_extension} не поддерживается",
            )
            return False
        if int(file.size / 2**20) > size_limit:
            form.add_error(
                field_name,
                f"""Размер загружаемого файла не должен превышать {size_limit} MB,
                ваш файл весит {int(file.size / 2 ** 20)} MB.""",
            )
            return False
    return True
