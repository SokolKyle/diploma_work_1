from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())


class BlogAdminModel(admin.ModelAdmin):  # Переименован класс
    form = BlogAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'time_created', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_created')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'helpful')
    list_filter = ('blog', 'user')
    search_fields = ('user__username',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    list_filter = ('blog', 'user', 'created_at')
    search_fields = ('user__username', 'content')


admin.site.register(Blog, BlogAdminModel)  # Обновлено для использования нового имени
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)
