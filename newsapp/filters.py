from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFilter
from .models import Post
from django.utils.translation import gettext_lazy as _

class PostFilter(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains',
                       label=_('Заголовок')
                       )
    category_type = ChoiceFilter(field_name='category_type',
                                 choices=Post.CATEGORY_CHOICES,
                                 label=_('Категория'),
                                 empty_label=_('Все категории')
                                 )
    created_at = DateFilter(field_name='created_at',
                            lookup_expr='gte',
                            widget=forms.DateInput(attrs={'type': 'date'}),
                            label=_('Дата публикации')
                            )

    class Meta:
        model = Post
        fields = ['title',
                  'category_type',
                  'created_at'
                  ]
