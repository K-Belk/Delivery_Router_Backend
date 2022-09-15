from rest_framework import serializers
from deliveries.models import Delivery_Location, Deliveries


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_Location
        fields = '__all__'

class KeySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)

class DeliverySerializer(serializers.ModelSerializer):


    class Meta:
        model = Deliveries
        fields = '__all__'
        depth = 2
