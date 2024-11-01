import uuid

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.serializers import SignupSerializer, TokenSerializer


class SignUpViewSet(CreateModelMixin, GenericViewSet):
    """Вьюсет для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if instance.email != email:
                raise ValidationError('У данного пользователя другая почта!')
            serializer.is_valid(raise_exception=False)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data['email']

        code = uuid.uuid4()

        send_mail(
            'КОД ПОДТВЕРЖДЕНИЯ',
            f'Ваш код подтверждения!\n{code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        instance.confirmation_code = code
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(TokenObtainPairView):
    """Вьюсет для получения ТОКЕНА"""
    serializer_class = TokenSerializer
