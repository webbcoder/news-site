from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm


# Create your views here.

class SiteLoginView(LoginView):
    template_name = 'news/login.html'


@login_required
def profile(request):
    return render(request, 'news/profile.html')


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        # posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query) | Q(is_moderation=True))
    else:
        posts = Post.objects.all()
        # posts = Post.objects.filter(is_moderation=True)
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    return render(request, 'news/index.html',
                  context={
                      'page_object': page,
                      'is_paginated': is_paginated,
                      'prev_url': prev_url,
                      'next_url': next_url
                  })


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'news/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'news/post_create.html'
    raise_exception = True
    # post = Post(is_moderation=False)
    # post.save()




class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'news/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'news/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'news/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'news/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'news/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'news/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'news/tags_list.html', context={'tags': tags})
