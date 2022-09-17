import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import EditionChoices, ProductChoices, Delivery_Location, Deliveries

from django.contrib.auth.models import User


class DeliveriesTest(APITestCase):

    def setUp(self):

        self.delivery_url = reverse('deliveries-list')
        
        ProductChoices.objects.create(product = 'Nacho creations magazine')
        ProductChoices.objects.create(product = 'Super spicy salsa magazine')

        product_query = ProductChoices.objects.all().values()
        self.product_one_id = product_query[0]['id']
        self.product_two_id = product_query[1]['id']

        EditionChoices.objects.create(
            edition = 'Ski season',
            year = 2020,
            product = ProductChoices.objects.get(id=self.product_one_id)
        )
        EditionChoices.objects.create(
            edition = 'Cycle season',
            year = 2003,
            product = ProductChoices.objects.get(id=self.product_two_id)
        )

        edition_query = EditionChoices.objects.all().values()
        self.edition_one_id = edition_query[0]['id']
        self.edition_two_id = edition_query[1]['id']

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
        delivery_query = Delivery_Location.objects.all().values()
        self.location_one_id = delivery_query[0]['id']
        self.location_two_id = delivery_query[1]['id']

        User.objects.create(
            username = "Tacocat",
            email = "tacocat@emai.com",
            first_name = "Bob",
            last_name = "Barker"
        )
        
        driver_query = User.objects.all().values()
        self.driver_one_id = driver_query[0]['id']        

        self.delivery_data = {
            "amount" : 24,
            "date" : "2022-9-17",
            "driver" : self.driver_one_id,
            "edition" : self.edition_one_id,
            "product" : self.product_one_id,
            "location" : self.location_one_id
        }
        
    def test_create_delivery(self):

        response = self.client.post(self.delivery_url, json.dumps(self.delivery_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_amount_delivery(self):

        invalid_amount_data = self.delivery_data
        invalid_amount_data['amount'] = -10

        response = self.client.post(self.delivery_url, json.dumps(invalid_amount_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_delivery(self):

        invalid_date_data = self.delivery_data
        invalid_date_data['date'] = '9-17-2022'

        response = self.client.post(self.delivery_url, json.dumps(invalid_date_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_driver_delivery(self):

        invalid_driver_data = self.delivery_data
        invalid_driver_data['driver'] = self.driver_one_id + 1

        response = self.client.post(self.delivery_url, json.dumps(invalid_driver_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_edition_delivery(self):

        invalid_edition_data = self.delivery_data
        invalid_edition_data['edition'] = self.edition_two_id + 1

        response = self.client.post(self.delivery_url, json.dumps(invalid_edition_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_product_delivery(self):

        invalid_product_data = self.delivery_data
        invalid_product_data['product'] = self.product_two_id + 1

        response = self.client.post(self.delivery_url, json.dumps(invalid_product_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_location_delivery(self):

        invalid_location_data = self.delivery_data
        invalid_location_data['location'] = self.location_two_id + 1

        response = self.client.post(self.delivery_url, json.dumps(invalid_location_data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_deliveries(self):

        response = self.client.get(self.delivery_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_product(self):

        self.client.post(self.delivery_url, json.dumps(self.delivery_data), content_type='application/json')
        self.client.post(self.delivery_url, json.dumps(self.delivery_data), content_type='application/json')
        self.client.post(self.delivery_url, json.dumps(self.delivery_data), content_type='application/json')

        query = Deliveries.objects.all().values()
        id = query[0]['id']
        response = self.client.get(f'{self.delivery_url}{id}/')
        self.assertEqual(response.data['id'], id)