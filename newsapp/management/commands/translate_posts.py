from django.core.management.base import BaseCommand
from newsapp.models import Post

class Command(BaseCommand):
    help = 'Translate first five posts'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()[:5]
        for post in posts:
            post.title_en = f'{post.title} (translated)'
            post.text_en = f'{post.text} (translated)'
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully translated first five posts'))