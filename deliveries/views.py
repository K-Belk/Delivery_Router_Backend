
import json
from .models import Delivery_Location, Deliveries, ProductChoices, EditionChoices
from rest_framework import viewsets, response
from .serializers import  DeliverySerializer, KeySerializer, LocationsSerializer, ProductSerializer, EditionSerializer

import environ

from rest_framework import permissions


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

class LocationsVewSet(viewsets.ModelViewSet):
    queryset = Delivery_Location.objects.all()
    serializer_class = LocationsSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer

    # def create(self, request):
    #     data = {
    #         # 'driver': request.user.pk,
    #         'driver': request.data['driver'],
    #         'date' : request.data['date'],
    #         'edition': int(request.data['edition']), 
    #         'product': int(request.data['product']),
    #         'amount' : int(request.data['amount']),
    #         'location': int(request.data['location']) ,
    #     }
        
    #     serializer = self.get_serializer(data= data)
    #     # print(data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return response.Response(serializer.data)

    # def retrieve(self, request, pk):
    #     data = Deliveries.objects.filter(location_id=pk)
    #     serializer = DeliverySerializer(data, many=True)
    #     return response.Response(serializer.data)

    # def update(self, request, pk):
    #     print(request.data)

class GoogleApiKeyViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        serializer = KeySerializer(
            instance = {'key': env('GOOGLE_KEY')}
        )
        return response.Response(serializer.data)

class RoutingKeyViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        serializer = KeySerializer(
            instance = {'key': env('ROUTING_KEY')}
        )
        return response.Response(serializer.data)

class MapKeyViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        serializer = KeySerializer(
            instance = {'key': env('MAP_KEY')}
        )
        return response.Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):

    queryset = ProductChoices.objects.all()
    serializer_class = ProductSerializer

class EditionViewSet(viewsets.ModelViewSet):

    queryset = EditionChoices.objects.all()
    serializer_class = EditionSerializer
