from django.contrib import admin
from api.constanst import PER_PAGE
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
