import pytest
import json
from model_bakery import baker
from django.urls import reverse
from django_mock_queries.query import MockSet
from deliveries.models import Deliveries
from deliveries.views import DeliveryViewSet

pytestmark = pytest.mark.unit

class TestDeliveryViewSet:

    def test_list(self, mocker, rf, db):
        url = reverse('deliveries-list')
        request = rf.get(url)
        qs = MockSet(
            baker.make(Deliveries),
            baker.make(Deliveries),
            baker.make(Deliveries),
        )
        view = DeliveryViewSet.as_view(
            {'get' : 'list'}
        )

        mocker.patch.object(
            DeliveryViewSet, 'get_queryset', return_value=qs
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf, new_delivery_dict):
        url = reverse('deliveries-detail', args=[new_delivery_dict['delivery'].id])
        expected_json = new_delivery_dict['delivery_response']
        request = rf.get(url)
        mocker.patch.object(
            DeliveryViewSet, 'get_queryset', return_value=MockSet(new_delivery_dict['delivery'])
        )
        view = DeliveryViewSet.as_view(
            {'get' : 'retrieve' }
        )

        response = view(request, pk=new_delivery_dict['delivery'].id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_create(self, mocker, rf, prepare_delivery_dict):
        url = reverse('deliveries-list')
        valid_data_dict = prepare_delivery_dict['delivery_response']
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(prepare_delivery_dict['delivery_dict'])
        )
        mocker.patch.object(
            Deliveries, 'save'
        )
        view = DeliveryViewSet.as_view(
            {'post' : "create"}
        )

        response = view(request).render()

        valid_data_dict['id'] = response.data['id']
        assert response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf, new_delivery, prepare_delivery_dict):
        old_delivery = new_delivery
        delivery_dict = prepare_delivery_dict['delivery_dict']
        valid_data_dict = prepare_delivery_dict['delivery_response']

        url = reverse('deliveries-detail', args=[old_delivery.id])
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(delivery_dict)
        )
        mocker.patch.object(
            DeliveryViewSet, 'get_object', return_value=old_delivery
        )
        mocker.patch.object(
            Deliveries, 'save'
        )
        view = DeliveryViewSet.as_view(
            {'put' : 'update'}
        )

        response = view(request, pk=old_delivery.id).render()
        valid_data_dict['id'] = response.data['id']

        assert response.status_code == 200
        assert json.loads(response.content) == valid_data_dict

    @pytest.mark.parametrize('field', [
        ('driver'),
        ('edition'),
        ('product'),
        ('amount'),
        ('location'),
        ('date')
    ])
    def test_partial_update(self, mocker, rf, field, new_delivery, prepare_delivery_dict):
        old_delivery = new_delivery
        delivery_dict = prepare_delivery_dict['delivery_dict']

        valid_data = delivery_dict[field]
        url = reverse('deliveries-detail', args=[old_delivery.id])
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: valid_data})
        )
        mocker.patch.object(
            DeliveryViewSet, 'get_object', return_value=old_delivery
        )
        mocker.patch.object(
            Deliveries, 'save'
        )
        view = DeliveryViewSet.as_view(
            {'patch' : 'partial_update'}
        )

        response = view(request, pk=old_delivery.id).render()

        assert response.status_code == 200
        assert json.loads(response.content)[field] == prepare_delivery_dict['delivery_response'][field]

    def test_delete(self, mocker, rf, new_delivery):
        
        url = reverse('deliveries-detail', args=[new_delivery.id])
        request = rf.delete(url)
        mocker.patch.object(
            DeliveryViewSet, 'get_object', return_value=new_delivery
        )
        del_mock = mocker.patch.object(
            Deliveries, 'delete'
        )
        view = DeliveryViewSet.as_view(
            {'delete' : 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        assert del_mock.assert_called