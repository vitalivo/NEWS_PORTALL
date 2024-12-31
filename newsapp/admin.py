from django.contrib import admin
from .models import Author, Category, PostCategory, Comment, Post, Subscriber
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    model = Post
    
    
class CategoryAdmin(TranslationAdmin):
    model = Category
    
    
class CommentAdmin(TranslationAdmin):
    model = Comment
    
    
class SubscriberAdmin(TranslationAdmin):
    model = Subscriber
    

class AuthorAdmin(TranslationAdmin):
    model = Author
    

class PostCategoryAdmin(TranslationAdmin):
    model = PostCategory    
                

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Subscriber)
