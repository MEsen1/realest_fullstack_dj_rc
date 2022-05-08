from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from .models import Realtor
from .serializers import RealtorSerializer


class RealtorListView(ListAPIView):
    # * we dont want to make people get authorized to view
    permission_classes = (permissions.AllowAny,)
    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer
    # *by default any page will be paginated
    pagination_class = None


class RealtorRetrieveView(RetrieveAPIView):

    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer


class TopSellerView(ListAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = Realtor.objects.filter(top_seller=True)
    serializer_class = RealtorSerializer
    pagination_class = None
