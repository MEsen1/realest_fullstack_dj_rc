from dataclasses import fields
from rest_framework import serializers
from .models import Realtor


class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtor
        fields = (
            "id",
            "name",
            "photo",
            "description",
            "phone",
            "email",
            "top_seller",
            "date_hired",
        )
