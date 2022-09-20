
import json

from deliveries.external_api_calls import GoogleCalls
from .models import Delivery_Location, Deliveries, ProductChoices, EditionChoices
from rest_framework import viewsets, response
from .serializers import  DeliverySerializer, KeySerializer, LocationsSerializer, ProductSerializer, EditionSerializer
import googlemaps

import environ

from rest_framework import permissions


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

google_call = GoogleCalls()


class LocationsVewSet(viewsets.ModelViewSet):
    queryset = Delivery_Location.objects.all()
    serializer_class = LocationsSerializer

    def create(self, request):
        
        location_info = google_call.places(request.data)
        # print(location_info['status'])
        if location_info['status']['request_status'] == 'valid' and location_info['status']['business_status'] == 'OPERATIONAL':

            data = {
                "name" : location_info['name'],
                "street" : request.data['street'],
                "suite" : request.data['suite'],
                "city" : request.data['city'],
                "state" : request.data['state'],
                "postal_code" : request.data['postal_code'],
                "latitude" : location_info['latitude'],
                "longitude" : location_info['longitude'],
                "notes" : request.data['notes'],
                "phone" : location_info['phone'],
                "hours" : location_info['hours'],
            }

            serializer = LocationsSerializer(data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return response.Response({'created' : serializer.data}, status = 201)
            else:
                return response.Response({'error' : serializer.errors}, status=400 )
        else:
            if location_info['status']['request_status'] != 'valid':
                return response.Response({'error' : location_info['status']['request_status']}, status=400 )
            else:
                return response.Response({'error' : location_info['status']['business_status']}, status=400 )


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer

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
