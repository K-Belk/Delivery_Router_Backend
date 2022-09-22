import json
import pytest
from model_bakery import baker
from django.urls import reverse
from deliveries.models import Delivery_Location
from deliveries.views import google_call

pytestmark = pytest.mark.django_db

class TestLocationsEndpoints:

    endpoint = reverse('locations-list')

    def test_list(self, api_client):
        baker.make(Delivery_Location, _quantity=3)

        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client, monkeypatch, prepare_location_dict):
        location = prepare_location_dict['location']
        def g_call_mock_data(data):
            return {'status': {'request_status': 'valid',
                            'business_status':'OPERATIONAL'
                            },
                            'name' : location.name,
                            'latitude' : location.latitude,
                            'longitude' : location.longitude,
                            'phone' : location.phone,
                            'hours' : location.hours,
                            }
        monkeypatch.setattr(google_call, 'places', g_call_mock_data)
        input_json = {
            'name' : location.name,
            'street' : location.street,
            'suite' : location.suite,
            'city' : location.city,
            'state' : location.state,
            'postal_code' : location.postal_code,
            'notes' : location.notes,
        }

        expected_json = prepare_location_dict['location_dict']

        response = api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
            )

        assert response.status_code == 201
        expected_json['created']['id'] = response.data['created']['id']
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field', [
        ("name"),
        ("street"),
        ("city"),
        ("state"),
        ("postal_code"),
    ])
    def test_invalid_location(self, field, api_client, monkeypatch, prepare_location_dict):
        location = prepare_location_dict['location_dict']['created']
        location[field] = ''
        def g_call_mock_data(data):
            return {'status': {'request_status': 'valid',
                            'business_status':'OPERATIONAL'
                            },
                            'name' : location['name'],
                            'latitude' : location['latitude'],
                            'longitude' : location['longitude'],
                            'phone' : location['phone'],
                            'hours' : location['hours'],
                            }
        monkeypatch.setattr(google_call, 'places', g_call_mock_data)
        input_json = {
            'name' : location['name'],
            'street' : location['street'],
            'suite' : location['suite'],
            'city' : location['city'],
            'state' : location['state'],
            'postal_code' : location['postal_code'],
            'notes' : location['notes'],
        }

        response =api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
            )

        assert response.status_code == 400

    def test_retrieve(self, api_client, new_location_dict):
        location = new_location_dict['location']
        expected_json = new_location_dict['location_dict']

        url = f'{self.endpoint}{location.id}/'
        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, prepare_location_dict):
        old_location = baker.make(Delivery_Location)
        prepare_location_dict['location']
        location_dict = prepare_location_dict['location_dict']['created']
        location_dict['id'] = old_location.id

        url = f'{self.endpoint}{old_location.id}/'
        response = api_client().put(url, location_dict, format='json')
        assert response.status_code == 200
        assert json.loads(response.content) == location_dict

    @pytest.mark.parametrize('field', [
        ("name"),
        ("street"),
        ("suite"),
        ("city"),
        ("state"),
        ("postal_code"),
        ("latitude"),
        ("longitude"),
        ("notes"),
        ("phone"),
        ("hours"),
    ])
    def test_partial_update(self, field, api_client, prepare_location_dict):
        old_location = baker.make(Delivery_Location)
        prepare_location_dict['location']
        location_dict = prepare_location_dict['location_dict']['created']

        valid_data = location_dict[field]
        url = f'{self.endpoint}{old_location.id}/'
        response = api_client().patch(url, {field: valid_data}, format='json')

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_data

    def test_delete(self, api_client):
        location = baker.make(Delivery_Location)
        url = f'{self.endpoint}{location.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Delivery_Location.objects.all().count() == 0

