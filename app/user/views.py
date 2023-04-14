from user.seralizers import UserSerializer
from rest_framework import generics


class CreateUser(generics.CreateAPIView):
    """Create new user during registration process."""

    serializer_class = UserSerializer
