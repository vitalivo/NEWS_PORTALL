from django.contrib.auth.models import User
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def product_created(instance, created, **kwargs):
    if not created:
        return

    categories = instance.categories.all()
    if categories:
        first_category = categories[0]
    else:
        first_category = None

    if first_category:
        subscribers = User.objects.filter(categories__in=[first_category])
        emails = subscribers.values_list('email', flat=True)
        subject = f'Новая статья в категории {first_category.name}'
        text_content = (
            f'Новая статья в категории {first_category.name}\n'
            f'Название: {instance.title}\n'
            f'Текст: {instance.text}\n'
            f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Новая статья в категории {first_category.name}<br>'
            f'Название: {instance.title}<br>'
            f'Текст: {instance.text}<br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на статью</a>'
        )

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, 'vitalivoloshin1975@yandex.co.il', [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()