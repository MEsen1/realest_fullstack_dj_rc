from email.policy import HTTP
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Contact
from rest_framework import serializers
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer


class ContactCreateView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer

    def post(self, request, format=None):

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            send_mail(
                data["subject"],
                "Name:" + data["name"] + "\nEmail:" + data["email"] + "\n\nMessage:\n" + data["message"],
                "otonom3@gmail.com",
                recipient_list=(data["email"],),
                fail_silently=False,
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"error message {e}")
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     send_mail(
        #         data["subject"],
        #         "Name:" + data["name"] + "\nEmail:" + data["email"] + "\n\nMessage:\n" + data["message"],
        #         "otonom3@gmail.com",
        #         fail_silently=False,
        #     )

        #     # contact = Contact(name=data["name"], email=data["email"], subject=data["subject"], message=data["message"])
        #     # contact.save()
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)

        # except:
        #     return Response(serializer.errors, status=status.)
