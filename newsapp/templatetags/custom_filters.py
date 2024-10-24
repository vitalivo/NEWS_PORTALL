from django import template
from django_filters import FilterSet





register = template.Library()

BAD_WORDS = ['редиска', 'дурак', 'идиот']  # Список нежелательных слов


@register.filter(name='censor')
def censor(value):
    """
    Заменяет все нежелательные слова из списка BAD_WORDS на символы '*'.
    """
    if not isinstance(value, str):
        raise TypeError("Censor filter expects a string input")
    words = value.split()
    censored_text = []

    for word in words:
        clean_word = word.lower()  # Приводим слово к нижнему регистру для сравнения
        for bad_word in BAD_WORDS:
            if bad_word in clean_word:
                word = word[0] + '*' * (len(word) - 1)  # Замена всех букв на '*', кроме первой
        censored_text.append(word)

    return ' '.join(censored_text)



