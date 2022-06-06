from .models import City_State,Addresses,Delivery_Location,Delivery_Season,Deliveries
from rest_framework import viewsets, response
from .serializers import AddressesSerializer, CityStateSerializer, KeySerializer, LocationsSerializer
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class CityStateVewSet(viewsets.ModelViewSet):
    queryset = City_State.objects.all()
    serializer_class = CityStateSerializer

    # def retrieve(self, request, pk=None):
    #     print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #     print(request)
    #     print(pk)

    #     return 

class AddressesVewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressesSerializer

class LocationsVewSet(viewsets.ModelViewSet):
    queryset = Delivery_Location.objects.all()
    serializer_class = LocationsSerializer

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