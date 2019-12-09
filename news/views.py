from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import View, CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AdvUser, Post, Tag
from .utils import *
from .forms import RegisterUserForm, ChangeUserInfoForm, TagForm, PostForm
from django.core.signing import BadSignature


# Create your views here.

class SiteLoginView(LoginView):
    template_name = 'news/login.html'


class SiteLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'news/logout.html'


@login_required
def profile(request):
    return render(request, 'news/profile.html')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'news/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('news:profile')
    success_message = 'Personal data of user was changed'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class SitePasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'news/password_change.html'
    success_url = reverse_lazy('news:profile')
    success_message = 'Password of user was changed'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'news/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('news:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'news/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'news/delete user.html'
    success_url = reverse_lazy('news:posts_list_url')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User was deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'news/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'news/user_is_activated.html'
    else:
        template = 'news/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user. save()
    return render(request, template)


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
