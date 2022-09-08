import json
from .models import City_State,Addresses,Delivery_Location,Delivery_Season,Deliveries
from rest_framework import viewsets, response
from .serializers import AddressesSerializer, CityStateSerializer, DeliverySerializer, KeySerializer, LocationsSerializer
from django.contrib.auth.models import User

import environ

from rest_framework import permissions


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class CityStateVewSet(viewsets.ModelViewSet):
    queryset = City_State.objects.all()
    serializer_class = CityStateSerializer

class AddressesVewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressesSerializer

class LocationsVewSet(viewsets.ModelViewSet):
    queryset = Delivery_Location.objects.all()
    serializer_class = LocationsSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer

    def create(self, request):

        serializer = self.get_serializer(
        data = {
            'driver': request.user.pk,
            'lnk_delivery': int(request.data['lnk_delivery']), 
            'fifty_five_delivery': int(request.data['fifty_five_delivery']),
            'location': int(request.data['location']) ,
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(serializer.data)

    def retrieve(self, request, pk):
        data = Deliveries.objects.filter(location_id=pk)
        serializer = DeliverySerializer(data, many=True)
        return response.Response(serializer.data)

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