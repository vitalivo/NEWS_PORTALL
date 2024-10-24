from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'category_type',
        ]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError('Заголовок не должен быть меньше 10 символов')
        if title[0].islower():
            raise ValidationError('Заголовок должен начинаться с заглавной буквы')
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 20:
            raise ValidationError('Текст не должен быть меньше 20 символов')
        if text[0].islower():
            raise ValidationError('Текст должен начинаться с заглавной буквы')
        return text

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')

        if text == title:
            raise ValidationError('Заголовок и текст не могут совпадать')

        return cleaned_data


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author'
        ]



