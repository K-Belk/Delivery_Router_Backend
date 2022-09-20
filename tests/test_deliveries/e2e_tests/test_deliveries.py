import json
import pytest
from model_bakery import baker
from django.urls import reverse
from deliveries.models import Deliveries

pytestmark = pytest.mark.django_db

class TestDeliveryEndpoints:

    endpoint = reverse('deliveries-list')

    def test_list(self, api_client):
        baker.make(Deliveries, _quantity=3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client, prepare_delivery_dict):
        input_json = prepare_delivery_dict['delivery_dict']
        expected_json = prepare_delivery_dict['delivery_response']
        response = api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
        )
        assert response.status_code == 201
        expected_json['id'] = response.data['id']
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field', [
        ('driver'),
        ('edition'),
        ('product'),
        ('amount'),
        ('location')
    ])
    def test_invalid_create(self, api_client, field, prepare_delivery_dict):
        input_json = prepare_delivery_dict['delivery_dict']
        input_json[field] = ''
        response =api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
            )
        assert response.status_code == 400

    def test_retrieve(self, api_client, new_delivery_dict):

        delivery = new_delivery_dict['delivery']
        expected_json = new_delivery_dict['delivery_response']
        url = f'{self.endpoint}{delivery.id}/'
        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, new_delivery, prepare_delivery_dict):

        old_delivery = new_delivery
        delivery_dict = prepare_delivery_dict['delivery_dict']
        expected_json = prepare_delivery_dict['delivery_response']
        delivery_dict['id'] = old_delivery.id
        expected_json['id'] = old_delivery.id
        url = f'{self.endpoint}{old_delivery.id}/'

        response = api_client().put(url, delivery_dict, format='json')
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field', [
        ('driver'),
        ('edition'),
        ('product'),
        ('amount'),
        ('location'),
        ('date')
    ])
    def test_partial_update(self, field, api_client, prepare_delivery_dict):
        old_delivery = baker.make(Deliveries)
        delivery_dict = prepare_delivery_dict['delivery_dict']

        valid_data = delivery_dict[field]

        url = f'{self.endpoint}{old_delivery.id}/'
        response = api_client().patch(url, {field: valid_data}, format='json')

        assert response.status_code == 200
        assert json.loads(response.content)[field] == prepare_delivery_dict['delivery_response'][field]

    def test_delete(self, api_client):
        
        delivery = baker.make(Deliveries)
        url = f'{self.endpoint}{delivery.id}/'
        response = api_client().delete(url)
        assert response.status_code == 204
        assert Deliveries.objects.all().count() == 0