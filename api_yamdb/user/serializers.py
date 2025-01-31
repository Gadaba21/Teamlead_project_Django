from django.contrib.auth.tokens import default_token_generator as dtg
from rest_framework.exceptions import NotFound, ValidationError as VE
from rest_framework.serializers import (CharField, EmailField,
                                        ModelSerializer, Serializer)
from rest_framework_simplejwt.tokens import AccessToken
from django.db import IntegrityError

from api.constants import MAX_EMAIL_FIELD, MAX_NAME_FIELD, UNIQUE_FIELDS
from .utils import send_confirmation_email
from .validators import validate_username, UsernameValidator
from .models import User


class SignUpSerializer(ModelSerializer):
    username = CharField(
        max_length=MAX_NAME_FIELD,
        validators=(validate_username, UsernameValidator(),)
    )
    email = EmailField(max_length=MAX_EMAIL_FIELD)

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        try:
            user, _ = User.objects.get_or_create(
                username=validated_data['username'],
                email=validated_data['email'],
            )
        except IntegrityError as e:
            error_message = str(e)
            if 'username' in error_message:
                raise VE({'username': [UNIQUE_FIELDS[1]]})
            else:
                if User.objects.filter(
                        username=validated_data['username']).exists():
                    raise VE({'username': [UNIQUE_FIELDS[1]],
                              'email': [UNIQUE_FIELDS[0]]})
                else:
                    raise VE({'email': [UNIQUE_FIELDS[0]]})

        send_confirmation_email(user.email, dtg.make_token(user))
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
        if not dtg.check_token(user, confirmation_code):
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
