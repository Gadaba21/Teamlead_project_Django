from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound, ValidationError as VE
from rest_framework.serializers import (CharField, EmailField,
                                        ModelSerializer, Serializer)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken

from api.constanst import MAX_EMAIL_FIELD, MAX_NAME_FIELD
from user.utils import generate_confirmation_code
from user.validators import validate_username, UsernameValidator

User = get_user_model()


class SignUpSerializer(ModelSerializer):
    username = CharField(
        max_length=MAX_NAME_FIELD,
        validators=(
            validate_username,
            UsernameValidator(),
            UniqueValidator(
                User.objects.all(),
                'Такой username уже существует.'
            )
        )
    )
    email = EmailField(
        max_length=MAX_EMAIL_FIELD,
        validators=(
            UniqueValidator(
                User.objects.all(),
                'Такой e-mail уже зарегистрирован.'
            ),
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


class TokenSerializer(Serializer):
    username = CharField()
    confirmation_code = CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound('Пользователь с таким именем не найден.')
        if user.confirmation_code != confirmation_code:
            raise VE('Неверный код подтверждения.', 'invalid_code')
        return {'user': user}

    def get_token(self, user):
        return AccessToken.for_user(user)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
