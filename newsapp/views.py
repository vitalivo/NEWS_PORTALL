from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post, Category
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin



from django.shortcuts import render
from .filters import PostFilter

def search(request):
    filterset = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'newsapp/news_search.html', {'filterset': filterset})


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'newsapp/news_list.html'
    context_object_name = 'news'
    paginate_by = 2

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


class NewsBaseCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        category_type = self.request.POST.get('category_type')
        post.category_type = category_type if category_type in ['AR', 'NW'] else 'NW'
        post.save()
        return HttpResponseRedirect(self.success_url)


class NewsBaseUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        category_type = self.request.POST.get('category_type')
        post.category_type = category_type if category_type in ['AR', 'NW'] else 'NW'
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