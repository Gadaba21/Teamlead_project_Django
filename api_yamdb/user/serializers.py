from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken

from api.constanst import MAX_EMAIL_FIELD, MAX_NAME_FIELD
from user.validators import validate_username
from user.utils import generate_confirmation_code

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_NAME_FIELD,
        validators=(validate_username, UniqueValidator(
            queryset=User.objects.all(),
            message='Такой username уже существует.')
        )
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_FIELD,
        validators=(UniqueValidator(
            queryset=User.objects.all(),
            message='Такой e-mail уже зарегистрирован.'),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.confirmation_code = generate_confirmation_code(user)
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        user = User.objects.filter(username=username).first()
        if not user or user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                'Неверный код подтверждения или имя пользователя.'
            )
        return {'user': user}

    def get_token(self, user):
        token = AccessToken.for_user(user)
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
