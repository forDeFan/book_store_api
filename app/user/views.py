"""User API views."""

from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from user.seralizers import (
    MyTokenObtainPairSerializer,
    RefreshTokenSerializer,
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """
    Create new user during registration process.
    User checkup in the db perform automatically
    (check if exist by email i.e.)
    """

    serializer_class: UserSerializer = UserSerializer


class LoginView(TokenObtainPairView):
    """
    API view to log in (obtain access and refresh token).
    """

    permission_classes: permissions = (AllowAny,)
    serializer_class: TokenObtainPairSerializer = (
        MyTokenObtainPairSerializer
    )


class LogoutView(generics.GenericAPIView):
    """
    API view to log out (refresh token blacklist).
    Access token will expire on setting defined time period itself.
    """
    serializer_class = RefreshTokenSerializer

    def post(self, request: Request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
