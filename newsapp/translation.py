from .models import Post, Category, Comment, Subscriber, Author, PostCategory
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'text',
        'author',
        'created_at',
        'rating',
        'category_type',
    )
    
    
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'subscribers',)
        
        
@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text', 'created_at', 'rating',)
    
    
@register(Subscriber)
class SubscriberTranslationOptions(TranslationOptions):
    fields = ('user', 'category',)  
    
    
@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('rating',)
    
    
@register(PostCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('post', 'category')    