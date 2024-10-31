from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class CategoryGenreMixin(CreateModelMixin,
                         DestroyModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    """Миксин для категорий и жанров."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
