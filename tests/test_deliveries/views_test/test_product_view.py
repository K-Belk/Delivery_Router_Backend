import pytest
import json
from model_bakery import baker
from django.urls import reverse
from django_mock_queries.query import MockSet
from deliveries.models import ProductChoices
from deliveries.views import ProductViewSet

pytestmark = pytest.mark.unit

class TestProductViewset:

    def test_list(self, mocker, rf, db):
        url = reverse('products-list')
        request = rf.get(url)
        qs = MockSet(
            baker.make(ProductChoices),
            baker.make(ProductChoices),
            baker.make(ProductChoices),
        )
        view = ProductViewSet.as_view(
            {'get' : 'list'}
        )

        mocker.patch.object(
            ProductViewSet, 'get_queryset', return_value=qs
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf, new_product_dict):
        url = reverse('products-detail', args=[new_product_dict['product'].id])
        expected_json = new_product_dict['product_dict']
        request = rf.get(url)
        mocker.patch.object(
            ProductViewSet, 'get_queryset', return_value=MockSet(new_product_dict['product'])
        )
        view = ProductViewSet.as_view(
            {'get' : 'retrieve' }
        )

        response = view(request, pk=new_product_dict['product'].id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_create(self, mocker, rf, prepare_product_dict):
        url = reverse('products-list')
        valid_data_dict = prepare_product_dict['product_dict']
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(prepare_product_dict['product_dict'])
        )
        mocker.patch.object(
            ProductChoices, 'save'
        )
        view = ProductViewSet.as_view(
            {'post' : "create"}
        )

        response = view(request).render()

        valid_data_dict['id'] = response.data['id']
        assert response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf, new_product, prepare_product_dict):
        old_product = new_product
        product_dict = prepare_product_dict['product_dict']
        
        url = reverse('products-detail', args=[old_product.id])
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(product_dict)
        )
        mocker.patch.object(
            ProductViewSet, 'get_object', return_value=old_product
        )
        mocker.patch.object(
            ProductChoices, 'save'
        )
        view = ProductViewSet.as_view(
            {'put' : 'update'}
        )

        response = view(request, pk=old_product.id).render()
        product_dict['id'] = response.data['id']

        assert response.status_code == 200
        assert json.loads(response.content) == product_dict

    def test_delete(self, mocker, rf, new_product):
        
        url = reverse('products-detail', args=[new_product.id])
        request = rf.delete(url)
        mocker.patch.object(
            ProductViewSet, 'get_object', return_value=new_product
        )
        del_mock = mocker.patch.object(
            ProductChoices, 'delete'
        )
        view = ProductViewSet.as_view(
            {'delete' : 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        assert del_mock.assert_called