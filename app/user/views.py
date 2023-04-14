from user.seralizers import UserSerializer
from rest_framework import generics


class CreateUser(generics.CreateAPIView):
    """
    Create new user during registration process.
    User checkup in the db perform automatically
    (check if exist by email i.e.)
    """

    serializer_class = UserSerializer
