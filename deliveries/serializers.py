from rest_framework import serializers
from deliveries.models import Delivery_Location, Deliveries, ProductChoices, EditionChoices
from django.contrib.auth.models import User


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_Location
        fields = '__all__'

class KeySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductChoices
        fields = '__all__'

class EditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = EditionChoices
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Deliveries
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(DeliverySerializer, self).to_representation(instance)

        driver_obj = list(User.objects.filter(id=ret['driver']).values())[0]
        driver_name = driver_obj['first_name'] + ' ' + driver_obj['last_name']if driver_obj else ''

        edition_obj = list(EditionChoices.objects.filter(id=ret['edition']).values())[0]
        edition_obj['product'] = list(ProductChoices.objects.filter(id=edition_obj['product_id']).values())[0]['product']
        edition_name = f"{edition_obj['edition']} {edition_obj['year']} {edition_obj['product']}" if edition_obj else ''

        product_obj = list(ProductChoices.objects.filter(id=ret['product']).values())

        location_obj = list(Delivery_Location.objects.filter(id=ret['location']).values())[0]

        extra_ret = {
            "driver" : driver_name,
            'edition' : edition_name,
            'product' : product_obj[0]['product'],
            'location' : {
                'name': location_obj['name'],
                'street': location_obj['street'],
                'suite': location_obj['suite'],
                'city': location_obj['city'],
                'state': location_obj['state'],
                'postal_code': location_obj['postal_code'],
            }

        }
        ret.update(extra_ret)
        return ret
