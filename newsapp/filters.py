from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFilter
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains',
                       label='Заголовок'
                       )
    category_type = ChoiceFilter(field_name='category_type',
                                 choices=Post.CATEGORY_CHOICES,
                                 label='Категория',
                                 empty_label='Все категории'
                                 )
    created_at = DateFilter(field_name='created_at',
                            lookup_expr='gte',
                            widget=forms.DateInput(attrs={'type': 'date'}),
                            label='Дата публикации'
                            )

    class Meta:
        model = Post
        fields = ['title',
                  'category_type',
                  'created_at'
                  ]

