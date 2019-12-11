from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.dispatch import Signal
from .utils import send_activation_notification, get_timestamp_path
from ckeditor.fields import RichTextField
# Create your models here.

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send notifications about new comments?')

    def delete(self, *args, **kwargs):
        for post in self.post_set.all():
            post.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = RichTextField(blank=True, null=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    author = models.ForeignKey(AdvUser, default=1, on_delete=models.CASCADE, verbose_name='Posted by')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Image')
    date_pub = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='List in?')
    is_moderation = models.NullBooleanField(default=False)

    def get_absolute_url(self):
        return reverse('news:post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('news:post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('news:post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.dlete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.title


class AdditionalImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name_plural = 'Additional illustrations'
        verbose_name = 'Additional illustration'


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('news:tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('news:tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('news:tag_delete_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
