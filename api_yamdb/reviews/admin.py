from django.contrib import admin
from api.constants import PER_PAGE

from .models import Category, Comment, Title, Review, Genre


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'score',
        'pub_date',
        'title'
    )
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = PER_PAGE
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'pub_date',
        'review'
    )
    list_filter = ('author', 'pub_date')
    list_per_page = PER_PAGE
    search_fields = ('author',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'category',
        'name',
        'year',
        'description'
    )
    list_display_links = ('name', 'description')
    list_editable = ('category',)
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'
