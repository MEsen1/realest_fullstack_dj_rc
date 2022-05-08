from multiprocessing import context
from typing import Any, Optional

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView  # known as concrete view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .models import UserAccount

from .serializers import LoginSerializer, LogoutSerializer, RegistrationSerializer, UserAccountSerializer


# api view is most generic, viewsets better for clearer CRUDs


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request: Request):
        """return a response after succesfull registrtion"""

        # serializer = self.get_serializer(data=request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request):
        """Return user after login"""
        user = request.data
        serializer = self.serializer_class(data=user)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(ViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]):
    def retrieve(self, request: Request, pk=None):
        """Return user on GET"""
        query = UserAccount.objects.get(id=pk)
        serializer = self.serializer_class(instance=query, context={"request": request})

        if not serializer.is_valid():
            return Response({"Fail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]):
        """Return updated user"""
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permissin_classes = (AllowAny,)

    def post(self, request: Request):
        """Validate token and save"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
