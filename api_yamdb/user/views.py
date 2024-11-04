from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.permissions import AdminOnly
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
from .utils import send_confirmation_email
from .models import User


class SignUpViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if (User.objects.filter(email=request.data.get(
            'email')).exists() and User.objects.filter(
                username=request.data.get('username')).exists()):
            existing_user = User.objects.get(username=request.data.get(
                'username'))
            context = {'email': existing_user.email,
                       'username': existing_user.username}
            return Response(context, status=HTTP_200_OK)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        send_confirmation_email(user.email, user.confirmation_code)
        context = {'email': user.email, 'username': user.username}
        return Response(context, HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data('user')
        token = serializer.get_token(user)
        return Response({'token': str(token)}, HTTP_200_OK)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(methods=('patch', 'get'), detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, HTTP_200_OK)
