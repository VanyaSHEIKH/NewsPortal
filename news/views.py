from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter,CategoryFilter
from .forms import *


class PostList(ListView):
    model = Post
    ordering = 'date_in'
    # template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-date_in')
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        return context

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_template_names(self):
        if self.request.path == '/news/create':
            return 'search.html'
        return 'news.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(CreateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'new_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post_type = 'AR'
        post.save()
        return super().form_valid(form)

    # def add_post(request):
    #     # Проверяем есть ли у данного пользователя разрешение для добавления поста
    #     # Если такого разрешения нет, то выкидываем исключение PermissionDenied
    #     if not request.user.has_perm('news.add_post'):
    #         raise PermissionDenied
    #     # Бизнес-логика для добавления поста


class PostUpdate(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'new_create.html'


class PostDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')


class PostSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'new_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class CategoryList(ListView):
    model = Category
    ordering = '-date_in'
    template_name = 'categories_list.html'
    context_object_name = 'categories'
    paginate_by = 2


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
    #     context['category'] = self.category
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = CategoryFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs



# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     message = "Подписка на категорию прошла успешно!"
#     return render(request, 'subscribe.html', {'category': category, 'message': message})


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('/')  # Замените на нужный URL
    else:
        form = SubscriptionForm()

    categories = Category.objects.all()
    return render(request, 'subscribe.html', {'form': form, 'categories': categories})