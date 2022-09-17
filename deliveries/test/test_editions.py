from datetime import date
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import EditionChoices, ProductChoices

class EditionTest(APITestCase):

    def setUp(self):
        
        ProductChoices.objects.create(product = 'Nacho creations magazine')
        ProductChoices.objects.create(product = 'Super spicy salsa magazine')

        self.edition_url = reverse('edition-list')

        self.product_query = ProductChoices.objects.all().values()
        self.product_one_id = self.product_query[0]['id']
        self.product_two_id = self.product_query[1]['id']
        
        self.edition_data = {
            'edition': 'February',
            'year': 2022,
            'product': self.product_one_id
            }

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


    def test_create_edition(self):

        response = self.client.post(self.edition_url, json.dumps(self.edition_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_edition_edition(self):

        invalid_edition_data = self.edition_data
        invalid_edition_data['edition'] = ''

        response_edition = self.client.post(self.edition_url, json.dumps(invalid_edition_data), content_type='application/json')
        self.assertEqual(response_edition.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_year_edition_low(self):

        invalid_year_data = self.edition_data
        invalid_year_data['year'] = 1999

        response_year = self.client.post(self.edition_url, json.dumps(invalid_year_data), content_type='application/json')
        self.assertEqual(response_year.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_year_edition_high(self):

        def current_year():
            return date.today().year

        invalid_year_data = self.edition_data
        invalid_year_data['year'] = current_year()+1

        response_year = self.client.post(self.edition_url, json.dumps(invalid_year_data), content_type='application/json')
        self.assertEqual(response_year.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_product_edition_nonexistent(self):

        nonexistent_product = len(self.product_query)

        invalid_product_data = self.edition_data
        invalid_product_data['product'] = nonexistent_product

        response_product = self.client.post(self.edition_url, json.dumps(invalid_product_data), content_type='application/json')
        self.assertEqual(response_product.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_editions(self):

        self.client.post(self.edition_url, json.dumps(self.edition_data), content_type='application/json')

        response = self.client.post(self.edition_url, json.dumps(self.edition_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_editions(self):

        response = self.client.get(self.edition_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_edition(self):

        query = EditionChoices.objects.all().values()
        id = query[0]['id']
        response = self.client.get(f'{self.edition_url}{id}/')
        self.assertEqual(response.data['id'], id)
