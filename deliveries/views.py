from .models import City_State,Addresses,Delivery_Location,Delivery_Season,Deliveries
from rest_framework import viewsets
from .serializers import AddressesSerializer, CityStateSerializer, LocationsSerializer



class CityStateVewSet(viewsets.ModelViewSet):
    queryset = City_State.objects.all()
    serializer_class = CityStateSerializer

class AddressesVewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressesSerializer

class LocationsVewSet(viewsets.ModelViewSet):
    queryset = Delivery_Location.objects.all()
    serializer_class = LocationsSerializer