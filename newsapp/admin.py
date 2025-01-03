from django.contrib import admin
from .models import Author, Category, PostCategory, Comment, Post, Subscriber
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from .forms import PostForm

# class PostAdmin(TranslationAdmin):
#     form = PostForm
#     model = Post
#     list_display = ('title', 'created_at')
    
    
# class CategoryAdmin(TranslationAdmin):
#     model = Category
#     list_display = ('name',)


# class CommentAdmin(TranslationAdmin):
#     model = Comment
#     list_display = ('user', 'post', 'text', 'created_at')


# class SubscriberAdmin(TranslationAdmin):
#     model = Subscriber
#     list_display = ('user', 'category')


# class AuthorAdmin(TranslationAdmin):
#     model = Author
#     list_display = ('user', 'rating')


# class PostCategoryAdmin(TranslationAdmin):
#     model = PostCategory
#     list_display = ('post', 'category')


# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(PostCategory, PostCategoryAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Subscriber, SubscriberAdmin)

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(Author)
admin.site.register(PostCategory)
