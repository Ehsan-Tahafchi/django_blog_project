from django.shortcuts import render, redirect, reverse
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import PostForm
from django.views import generic
from django.urls import reverse_lazy


class PostListView(generic.ListView):
    template_name = 'blog/posts_list.html'
    context_object_name = 'dbpost'

    def get_queryset(self):
        return Post.objects.filter(status='Published').order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/posts_detail.html'
    context_object_name = 'dbpost'


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_create.html'


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts_list_view')
