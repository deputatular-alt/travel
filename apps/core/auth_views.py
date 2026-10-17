from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .auth_serializers import (
    RegistrationResponseSerializer,
    RegistrationSerializer,
    UserSerializer,
)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegistrationSerializer,
        responses={status.HTTP_201_CREATED: RegistrationResponseSerializer},
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': {
                    'id': user.pk,
                    'username': user.get_username(),
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        user = request.user
        return Response(
            {
                'id': user.pk,
                'username': user.get_username(),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        )


@extend_schema(request=None, responses={status.HTTP_204_NO_CONTENT: None})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if hasattr(request.user, 'auth_token'):
        request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
