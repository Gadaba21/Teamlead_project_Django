from django.contrib.auth.tokens import default_token_generator as dtg
from rest_framework.exceptions import NotFound, ValidationError as VE
from rest_framework.serializers import (CharField, EmailField,
                                        ModelSerializer, Serializer)
from rest_framework_simplejwt.tokens import AccessToken

from api.constants import MAX_EMAIL_FIELD, MAX_NAME_FIELD, FORBIDDEN_EMAIL
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

    def create(self, valid_data):
        user_by_email = User.objects.filter(email=valid_data['email']).first()
        if user_by_email and user_by_email.username != valid_data['username']:
            raise VE(FORBIDDEN_EMAIL)
        try:
            user, created = User.objects.get_or_create(
                username=valid_data['username'],
                defaults={'email': valid_data['email']}
            )
            if not created and user.email != valid_data['email']:
                raise VE(FORBIDDEN_EMAIL)
        except Exception as e:
            raise VE(f'{e}')
        send_confirmation_email(user.email, dtg.make_token(user))
        return user

# class SignUpSerializer(ModelSerializer):
#     username = CharField(
#         max_length=MAX_NAME_FIELD,
#         validators=(validate_username, UsernameValidator(),)
#     )
#     email = EmailField(max_length=MAX_EMAIL_FIELD)

#     class Meta:
#         model = User
#         fields = ('username', 'email')

#     def validate(self, data):
#         """
#         Общая валидация для проверки уникальности email и username,
#         а также обязательности полей.
#         """
#         # Проверка обязательных полей
#         if 'username' not in data or not data.get('username'):
#             raise VE({"username": ["Это поле обязательно."]})
#         if 'email' not in data or not data.get('email'):
#             raise VE({"email": ["Это поле обязательно."]})

#         # Проверка уникальности email
#         user_by_email = User.objects.filter(email=data['email']).first()
#         if user_by_email and user_by_email.username != data['username']:
#             raise VE({"email": ["Пользователь с таким email уже существует."]})

#         # Проверка уникальности username
#         user_by_username = User.objects.filter(username=data['username']).first()
#         if user_by_username and user_by_username.email != data['email']:
#             raise VE({"username": ["Пользователь с таким именем уже существует!"]})

#         return data

#     def create(self, validated_data):
#         """
#         Создаем пользователя и отправляем email с кодом подтверждения.
#         """
#         try:
#             # Пытаемся создать или получить пользователя
#             user, created = User.objects.get_or_create(
#                 username=validated_data['username'],
#                 defaults={'email': validated_data['email']}
#             )

#             # Если пользователь уже существует, но email отличается, вызовем ошибку
#             if not created and user.email != validated_data['email']:
#                 raise VE({"email": ["Пользователь с таким email уже существует."]})

#         except Exception as e:
#             # Перехватываем другие исключения и возвращаем ошибку в нужном формате
#             raise VE({"error": [f"Ошибка создания пользователя: {str(e)}"]})

#         # Отправка email с кодом подтверждения
#         send_confirmation_email(user.email, dtg.make_token(user))
#         return user


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
