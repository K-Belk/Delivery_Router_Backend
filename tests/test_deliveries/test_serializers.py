import pytest
from deliveries.serializers import DeliverySerializer, LocationsSerializer, ProductSerializer, EditionSerializer

class TestProductSerializer:

    @pytest.mark.unit
    def test_serialize_model(self, new_product_dict):

        product = new_product_dict['product']
        expected_serialized_data = new_product_dict['product_dict']
        serializer = ProductSerializer(product)

        assert serializer.data
        assert serializer.data == expected_serialized_data

    @pytest.mark.unit
    def test_serialize_data(self, prepare_product_dict):

        valid_serialized_data = prepare_product_dict['product_dict']
        serializer = ProductSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

class TestEditionSerializer:

    @pytest.mark.unit
    def test_serialize_model(self, new_edition_dict):

        edition = new_edition_dict['edition']
        expected_serialized_data = new_edition_dict['edition_dict']
        serializer = EditionSerializer(edition)

        assert serializer.data
        assert serializer.data == expected_serialized_data


    @pytest.mark.unit
    def test_serialize_data(self, prepare_edition_dict):

        valid_serialized_data = prepare_edition_dict['edition_dict']
        serializer = EditionSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

class TestDeliverySerializer:

    @pytest.mark.unit
    def test_serialize_model(self, new_delivery_dict):

        delivery = new_delivery_dict['delivery']
        expected_serialized_data = new_delivery_dict['delivery_response']
        serializer = DeliverySerializer(delivery)

        assert serializer.data
        assert serializer.data == expected_serialized_data

    @pytest.mark.unit
    def test_serialize_data(self, prepare_delivery_dict):

        valid_serialized_data = prepare_delivery_dict['delivery_dict']
        serializer = DeliverySerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

class TestLocationsSerializer:

    @pytest.mark.unit
    def test_serialize_model(self, new_location_dict):

        location = new_location_dict['location']
        expected_serialized_data = new_location_dict['location_dict']
        serializer = LocationsSerializer(location)

        assert serializer.data
        assert serializer.data == expected_serialized_data

    @pytest.mark.unit
    def test_serialize_data(self, prepare_location_dict):

        valid_serialized_data = prepare_location_dict['location_dict']['created']
        serializer = LocationsSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}