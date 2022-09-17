import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Delivery_Location


class LocationsTest(APITestCase):

    def setUp(self):

        self.location_url = reverse('locations-list')
        self.location_data = {
        "name": "KVC Healthcare Nebraska",
        "street": "5555 Central Park ",
        "suite": "",
        "city": "Lincoln",
        "state": "NE",
        "postal_code": "68511",
        "latitude": "40.8159193",
        "longitude": "-96.65071329999999",
        "notes": ""
    }
    
        Delivery_Location.objects.create(
            name = 'test name',
            street = 'test street',
            city = 'test city',
            state = 'ts',
            postal_code = '12345',
            latitude = '40',
            longitude = '-96'
        )

        Delivery_Location.objects.create(
            name = 'test name two',
            street = 'test street two',
            city = 'test city two',
            state = 'ts',
            postal_code = '12345',
            latitude = '40',
            longitude = '-96'
        )

    def test_create_valid_location(self):
        
        response = self.client.post(self.location_url, json.dumps(self.location_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_name_location(self):

        invalid_name_data = self.location_data
        invalid_name_data['name'] = ''

        response_name = self.client.post(self.location_url, json.dumps(invalid_name_data), content_type='application/json')
        self.assertEqual(response_name.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_street_location(self):

        invalid_street_data = self.location_data
        invalid_street_data['street'] = ''

        response_street = self.client.post(self.location_url, json.dumps(invalid_street_data), content_type='application/json')

        self.assertEqual(response_street.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_city_location(self):

        invalid_city_data = self.location_data
        invalid_city_data['city'] = ''

        response_city = self.client.post(self.location_url, json.dumps(invalid_city_data), content_type='application/json')

        self.assertEqual(response_city.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_state_location(self):
        
        invalid_state_data = self.location_data
        invalid_state_data['state'] = ''
        invalid_state_length_data = self.location_data
        invalid_state_length_data['state'] = 'Nebraska'

        response_state = self.client.post(self.location_url, json.dumps(invalid_state_data), content_type='application/json')
        response_state_length = self.client.post(self.location_url, json.dumps(invalid_state_length_data), content_type='application/json')

        self.assertEqual(response_state.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_state_length.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_postal_code_location(self):

        invalid_postal_code_data = self.location_data
        invalid_postal_code_data['postal_code'] = ''
        
        response_postal_code = self.client.post(self.location_url, json.dumps(invalid_postal_code_data), content_type='application/json')

        self.assertEqual(response_postal_code.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_locations(self):

        self.client.post(self.location_url, json.dumps(self.location_data), content_type='application/json')
        response = self.client.post(self.location_url, json.dumps(self.location_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_locations(self):

        response = self.client.get(self.location_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_location(self):

        query = Delivery_Location.objects.all().values()
        id = query[0]['id']
        response = self.client.get(f'{self.location_url}{id}/')
        self.assertEqual(response.data['id'], id)

    