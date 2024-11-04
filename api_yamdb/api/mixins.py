from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet
from .permissions import AnonimReadOnly, AdminOnly


class CategoryGenreMixin(CreateModelMixin,
                         DestroyModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    """Миксин для категорий и жанров."""
    permission_classes = (AnonimReadOnly | AdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
