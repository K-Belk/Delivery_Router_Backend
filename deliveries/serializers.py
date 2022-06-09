from rest_framework import serializers
from deliveries.models import Addresses, City_State, Delivery_Location, Deliveries

class CityStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = City_State
        fields = ['id', 'city', 'state', 'postal_code']

class AddressesSerializer(serializers.ModelSerializer):
    city_and_state = CityStateSerializer(many=False)
    
    class Meta:
        model = Addresses
        fields = ['id', 'street', 'suite', 'city_and_state', 'latitude', 'longitude', 'notes' ]


class LocationsSerializer(serializers.ModelSerializer):
    address = AddressesSerializer(many=False)

    class Meta:
        model = Delivery_Location
        fields = ['id', 'name', 'address']

    def create(self, validated_data):
        location_data, address_data, city_state_data = self.destructure_location_valid_data(validated_data)
        new_city_state, city_state_created  = City_State.objects.get_or_create(**city_state_data)
        address_data['city_and_state'] = new_city_state
        new_address, address_created = Addresses.objects.get_or_create(**address_data)
        location_data['address'] = new_address
        new_location, location_created = Delivery_Location.objects.get_or_create(**location_data)
        return new_location 

    def update(self, instance, validated_data):
        location_instance = instance
        address_instance = Addresses.objects.get(id=location_instance.address_id)
        city_state_instance = City_State.objects.get(id=address_instance.city_and_state_id)
        location_data, address_data, city_state_data = self.destructure_location_valid_data(validated_data)
        city_state_updated = self.update_city_state(city_state_instance, city_state_data)
        address_updated = self.update_address(address_instance, address_data, city_state_updated)
        location_updated = self.update_location(location_instance, location_data, address_updated)
        return location_updated

    def destructure_location_valid_data(self, validated_data):
        location_data = dict(validated_data)
        address_data = dict(location_data.pop('address'))
        city_state_data= dict(address_data.pop('city_and_state'))
        return location_data, address_data, city_state_data
        
    def update_city_state(self, instance, validated_data):
        instance.city = validated_data['city']
        instance.state = validated_data['state']
        instance.postal_code = validated_data['postal_code']
        instance.save()
        return instance

    def update_address(self, instance, validated_data, city_and_state):
        instance.street = validated_data['street']
        instance.suite = validated_data['suite']
        instance.city_and_state = city_and_state
        instance.latitude = validated_data['latitude']
        instance.longitude = validated_data['longitude']
        instance.save()
        return instance

    def update_location(self, instance, validated_data, address):
        instance.name = validated_data['name']
        instance.address = address
        instance.save()
        return instance

class KeySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)

class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Deliveries
        fields = ['driver', 'lnk_delivery', 'fifty_five_delivery', 'location']
