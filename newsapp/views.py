from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post, Category, Subscriber
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from django.core.cache import cache


def search(request):
    filterset = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'newsapp/news_search.html', {'filterset': filterset})


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'newsapp/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class NewsDetail(DetailView):
    model = Post
    template_name = 'newsapp/news_detail.html'
    context_object_name = 'news'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.get_queryset())
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class NewsBaseCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        category_type = self.request.POST.get('category_type')
        post.category_type = category_type if category_type in [_('AR'), _('NW')] else _('NW')
        post.save()
        return HttpResponseRedirect(self.success_url)


class NewsBaseUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        category_type = self.request.POST.get('category_type')
        post.category_type = category_type if category_type in [_('AR'), _('NW')] else _('NW')
        post.save()
        return HttpResponseRedirect(self.success_url)


class NewsBaseDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('news_list')


class NewsCreate(LoginRequiredMixin, NewsBaseCreate):
    permission_required = ('newsapp.add_post',)
    raise_exception = True
    template_name = 'newsapp/news_create.html'


class NewsUpdate(LoginRequiredMixin, NewsBaseUpdate):
    permission_required = ('newsapp.change_post',)
    template_name = 'newsapp/news_edit.html'


class NewsDelete(LoginRequiredMixin, NewsBaseDelete):
    permission_required = ('newsapp.delete_post',)
    template_name = 'newsapp/news_delete.html'


class ArticlesCreate(LoginRequiredMixin, NewsBaseCreate):
    permission_required = ('newsapp.add_post',)
    raise_exception = True
    template_name = 'newsapp/articles_create.html'


class ArticlesUpdate(LoginRequiredMixin, NewsBaseUpdate):
    permission_required = ('newsapp.change_post',)
    template_name = 'newsapp/articles_edit.html'


class ArticlesDelete(LoginRequiredMixin, NewsBaseDelete):
    permission_required = ('newsapp.delete_post',)
    template_name = 'newsapp/articles_delete.html'


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
