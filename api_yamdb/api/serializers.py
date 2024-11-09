from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class BaseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')


class CategorySerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Category


class GenreSerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    """Сериализатор произведений, для чтения."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений, для изменений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def validate_genre(self, value):
        """Проверка, что поле genre не пустое."""
        if not value:
            raise serializers.ValidationError(
                "Поле 'genre' обязательно для заполнения.")
        return value

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleSerializerGet(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв можно оставить только один раз'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
