import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import ProductChoices

class ProductTest(APITestCase):

    def setUp(self):
        
        self.products_url = reverse('products-list')
        self.product_data = {'product':'Taco lovers magazine'}
        ProductChoices.objects.create(product = 'Nacho creations magazine')
        ProductChoices.objects.create(product = 'Super spicy salsa magazine')

    def test_create_product(self):

        response = self.client.post(self.products_url, json.dumps(self.product_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):

        invalid_product_data = self.product_data
        invalid_product_data['product'] = ''

        response = self.client.post(self.products_url, json.dumps(invalid_product_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_products(self):

        self.client.post(self.products_url, json.dumps(self.product_data), content_type='application/json')
        response = self.client.post(self.products_url, json.dumps(self.product_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_products(self):

        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_product(self):

        query = ProductChoices.objects.all().values()
        id = query[0]['id']
        response = self.client.get(f'{self.products_url}{id}/')
        self.assertEqual(response.data['id'], id)