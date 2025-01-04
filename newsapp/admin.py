from django.contrib import admin
from .models import Author, Category, PostCategory, Comment, Post, Subscriber
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from .forms import PostForm


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(Author)
admin.site.register(PostCategory)
