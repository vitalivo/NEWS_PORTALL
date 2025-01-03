# newsapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum([post.rating * 3 for post in self.post_set.all()])
        comment_rating = sum([comment.rating for comment in self.user.comment_set.all()])
        post_comment_rating = sum([comment.rating for post in self.post_set.all() for comment in post.comment_set.all()])
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, _('Article')),
        (NEWS, _('News')),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, help_text=_('Post type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts', through_fields=('post', 'category'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Вызвать сигнал post_save
        post_save.send(sender=self.__class__, instance=self, created=True)
        if cache.get(f'news-{self.pk}'):
            cache.delete(f'news-{self.pk}')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return f'/news/{self.pk}'

    # def get_absolute_url(self):
    #     return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return self.title[:10]


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


@receiver(m2m_changed, sender=Post.categories.through)
def send_notification(sender, instance, action, **kwargs):
    if action == "post_add":
        subscribers = Subscriber.objects.filter(category=instance.category)
        for subscriber in subscribers:
            send_mail(
                _(f"New post in {instance.category.name}"),
                _(f"Check out the new post: {instance.title} - {instance.get_absolute_url()}"),
                "vitalivoloshin1975@yandex.co.il",
                [subscriber.user.email],
                fail_silently=False,
            )
