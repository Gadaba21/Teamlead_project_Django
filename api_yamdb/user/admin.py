from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.decorators import register
from django.contrib.auth.models import Group

from user.models import User


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
    )
    search_fields = ('username', 'role', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'role',)
    list_editable = ('role',)
    list_display_links = ('username',)


site.empty_value_display = '-- Не задано --'
site.unregister(Group)
