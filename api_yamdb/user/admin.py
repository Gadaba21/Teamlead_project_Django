from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.decorators import display, register
from django.contrib.auth.models import Group

from .models import User
from reviews.models import Comment, Review


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'get_review_count',
        'get_comment_count',
    )

    @display(description='Количество рецензий')
    def get_review_count(self, obj):
        return Review.objects.filter(author=obj).count()

    @display(description='Количество комментариев')
    def get_comment_count(self, obj):
        return Comment.objects.filter(author=obj).count()

    search_fields = ('username', 'role', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'role',)
    list_editable = ('role',)
    list_display_links = ('username',)


site.empty_value_display = '-- Не задано --'
site.unregister(Group)
