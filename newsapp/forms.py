from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category_type',
            'author',
        ]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError(_('Title must be at least 10 characters long'))
        if title[0].islower():
            raise ValidationError(_('Title must start with an uppercase letter'))
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 20:
            raise ValidationError(_('Text must be at least 20 characters long'))
        if text[0].islower():
            raise ValidationError(_('Text must start with an uppercase letter'))
        return text

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')

        if text == title:
            raise ValidationError(_('Title and text cannot be the same'))

        return cleaned_data


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author'
        ]


