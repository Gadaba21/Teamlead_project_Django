from django.contrib.auth.tokens import default_token_generator as dtg
from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer, Serializer, ValidationError)

from api.constanst import MAX_LENGTH, MAX_NAME_FIELD
from user.models import User
from user.validators import UsernameValidator


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserCreationSerializer(Serializer):
    email = EmailField(required=True)
    username = CharField(validators=[UsernameValidator()], required=True)

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return attrs

    def validate_username(self, value):
        if value == "me":
            raise ValidationError('Имя пользователя "me" использовать нельзя!')
        return value


class TokenSerializer(Serializer):
    username = CharField(max_length=MAX_NAME_FIELD, required=True)
    confirmation_code = CharField(max_length=MAX_LENGTH, required=True)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise ValidationError(
                {'username': 'Пользователь с таким именем не найден'}
            )
        if not dtg.check_token(user, data['confirmation_code']):
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )
        return data
