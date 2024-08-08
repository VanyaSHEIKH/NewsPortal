from django.views.generic import ListView, DetailView
from .models import *
from datetime import datetime


class PostList(ListView):
    model = Post
    ordering = 'date_in'
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-date_in')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

