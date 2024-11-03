from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from user.serializers import SignUpSerializer, TokenSerializer
from user.utils import send_confirmation_email


class SignUpViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_confirmation_email(user.email, user.confirmation_code)
        context = {'email': user.email, 'username': user.username}
        return Response(context, status=HTTP_200_OK)


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.get_token(user)
        return Response({'token': str(token)}, status=HTTP_200_OK)
