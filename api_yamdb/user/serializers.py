# from django.contrib.auth.tokens import default_token_generator as dtg
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer, ValidationError, HiddenField)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

# from api.constanst import MAX_LENGTH, MAX_NAME_FIELD
from user.models import User
from user.validators import UsernameValidator


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class SignupSerializer(ModelSerializer):
    email = EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    username = CharField(
        validators=[UsernameValidator()],
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email",)

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


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = CharField(required=False)
        self.fields["password"] = HiddenField(default="")

    def get_token(self, user):
        return self.token_class.for_user(user)

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs["username"])

        if self.user.confirmation_code != attrs["confirmation_code"]:
            raise ValidationError("Неверный код подтверждения")

        data = str(self.get_token(self.user))
        return {"token": data}

    # username = CharField(max_length=MAX_NAME_FIELD, required=True)
    # confirmation_code = CharField(max_length=MAX_LENGTH, required=True)

    # def validate(self, data):
    #     try:
    #         user = User.objects.get(username=data['username'])
    #     except User.DoesNotExist:
    #         raise ValidationError(
    #             {'username': 'Пользователь с таким именем не найден'}
    #         )
    #     if not dtg.check_token(user, data['confirmation_code']):
    #         raise ValidationError(
    #             {'confirmation_code': 'Неверный код подтверждения'}
    #         )
    #     return data
