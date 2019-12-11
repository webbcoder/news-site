from django.contrib import admin
from .models import Post, AdvUser, AdditionalImage

# Register your models here.


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_pub')
    fields = (('tags', 'author'), 'title', 'body', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(Post, PostAdmin)
admin.site.register(AdvUser)
