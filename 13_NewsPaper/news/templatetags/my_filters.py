import re

from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name='censor')
def censor(value):
    # Проверка, что входной аргумент является строкой
    if not isinstance(value, str):
        raise TypeError("Входной аргумент должен быть строкой")

    # Список нецензурных слов, которые будем заменять
    censored_words = ["попа", "жопа", "какашки"]

    # Регулярное выражение для поиска нецензурных слов в тексте
    regex_pattern = r"\b(" + "|".join(map(re.escape, censored_words)) + r")\b"

    # Замена нецензурных слов на символы '*'
    censored_text = re.sub(regex_pattern, lambda match: match.group()[0] + '*' * (len(match.group()) - 1), value, flags=re.IGNORECASE)

    return censored_text


if __name__ == '__main__':
    # Пример использования
    print(censor("Жопа какАшки ПопА!"))  # Output: Ж*** и к****** в П***