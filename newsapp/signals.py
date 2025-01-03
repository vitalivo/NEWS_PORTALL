from django.contrib.auth.models import User
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

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
        subject = _('New article in category {category}').format(category=first_category.name)
        text_content = (
            _('New article in category {category}\n'
              'Title: {title}\n'
              'Text: {text}\n'
              'Link to the article: http://127.0.0.1:8000{url}').format(
                category=first_category.name,
                title=instance.title,
                text=instance.text,
                url=instance.get_absolute_url()
            )
        )
        html_content = (
            _('New article in category {category}<br>'
              'Title: {title}<br>'
              'Text: {text}<br>'
              '<a href="http://127.0.0.1:8000{url}">Link to the article</a>').format(
                category=first_category.name,
                title=instance.title,
                text=instance.text,
                url=instance.get_absolute_url()
            )
        )

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, 'vitalivoloshin1975@yandex.co.il', [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()