from django.db.models import Avg
from rest_framework import viewsets

from .filters import TitleFilters
from .mixins import CategoryGenreMixin

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerGet,
    TitleSerializerPost
)

from reviews.models import (
   Category,
   Comment,
   Genre,
   Review,
   Title
)


class CategoryViewSet(CategoryGenreMixin):
    """Вьюсет для модели категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """Вьюсет для модели жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        return TitleSerializerPost


class ReviewViewSet():
   pass


class TitleViewSet():
   pass
