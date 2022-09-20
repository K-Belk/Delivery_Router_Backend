import json
import pytest
from model_bakery import baker
from django.urls import reverse
from deliveries.models import ProductChoices

pytestmark = pytest.mark.django_db

class TestProductChoicesEndpoints:

    endpoint = reverse('products-list')

    def test_list(self, api_client):
        baker.make(ProductChoices, _quantity=3)

        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        product = baker.prepare(ProductChoices)
        
        input_json = {
            'product': product.product
        }
        expected_json = {
            'product': product.product
        }
        response = api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
        )
        assert response.status_code == 201
        expected_json['id'] = response.data['id']
        assert json.loads(response.content) == expected_json

    def test_invalid_create(self, api_client):
        baker.prepare(ProductChoices)
        
        input_json = {
            'product': ''
        }
        response = api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
        )
        assert response.status_code == 400

    def test_retrieve(self, api_client):
        product = baker.make(ProductChoices)
        expected_json = {
            'id' : product.id,
            'product' : product.product
        }
        url = f'{self.endpoint}{product.id}/'
        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client):
        old_product = baker.make(ProductChoices)
        new_product = baker.prepare(ProductChoices)
        product_dict = {
            'id' : old_product.id,
            'product' : new_product.product
        }
    
        url = f'{self.endpoint}{old_product.id}/'
        response = api_client().put(url, product_dict, format='json')
        assert response.status_code == 200
        assert json.loads(response.content) == product_dict

    def test_delete(self, api_client):
        product = baker.make(ProductChoices)
        url = f'{self.endpoint}{product.id}/'
        response = api_client().delete(url)
        assert response.status_code == 204
        assert ProductChoices.objects.all().count() == 0