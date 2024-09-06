from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Subscription
from .filters import PostFilter, CategoryFilter
from .forms import *
from django.contrib import messages
from django.conf import settings
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
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
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
    template_name = 'categories_list.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

#Рассылка уведомления на почту от подписке на категорию!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    subscription, created = Subscription.objects.get_or_create(user=user, category=category)

    if created:
        send_mail(
            'Подписка на категорию',
            f'Вы успешно подписались на категорию {category.name_category}.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, f'Вы успешно подписались на категорию {category.name_category}.')
    else:
        messages.warning(request, 'Вы уже подписаны на эту категорию.')

    return redirect('category_detail', pk=pk)
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    send_mail(
        'Подписка на категорию',
        f'Вы успешно подписались на категорию: {category.name_category}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f'Вы успешно подписались на категорию: {category.name_category}')
    return redirect(f'/news/category/{category.pk}')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    category.subscribers.remove(user)

    send_mail(
        'Отписка от категории',
        f'Вы успешно отписались от категории: {category.name_category}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f'Вы успешно отписались от категории: {category.name_category}')
    return redirect(f'/news/category/{category.pk}')

#
@login_required
def send_notification_email(user, Post):
    subject = f'Новая новость в категории {Post.category.name_category}'
    message = f'В категории "{Post.category.name_category}" добавлена новая новость: {Post.title}\n\n{Post.text}'
    recipient_list = [user.email]

    send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, recipient_list)

@login_required
def add_news_to_category(title, text, category):
    news = Post.objects.create(title=title, text=text, category=category)

    subscribers = Subscription.objects.filter(category=category).select_related('user')

    for subscription in subscribers:
        send_notification_email(subscription.user, news)