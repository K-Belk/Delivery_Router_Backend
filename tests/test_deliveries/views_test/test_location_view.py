import pytest
import json
from model_bakery import baker
from django.urls import reverse
from django_mock_queries.query import MockSet
from deliveries.models import Delivery_Location
from deliveries.views import LocationsVewSet
from deliveries.views import google_call


pytestmark = pytest.mark.unit

class TestLocationsVewSet:

    def test_list(self, mocker, rf, db):
        url = reverse('locations-list')
        request = rf.get(url)
        qs = MockSet(
            baker.make(Delivery_Location),
            baker.make(Delivery_Location),
            baker.make(Delivery_Location),
        )
        view = LocationsVewSet.as_view(
            {'get' : 'list'}
        )

        mocker.patch.object(
            LocationsVewSet, 'get_queryset', return_value=qs
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf, new_location_dict):
        url = reverse('locations-detail', args=[new_location_dict['location'].id])
        expected_json = new_location_dict['location_dict']
        request = rf.get(url)
        mocker.patch.object(
            LocationsVewSet, 'get_queryset', return_value=MockSet(new_location_dict['location'])
        )
        view = LocationsVewSet.as_view(
            {'get' : 'retrieve' }
        )

        response = view(request, pk=new_location_dict['location'].id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_create(self, mocker, rf, prepare_location_dict, monkeypatch):
        location = prepare_location_dict['location']
        url = reverse('locations-list')
        valid_data_dict = prepare_location_dict['location_dict']
        input_json = {
            'name' : location.name,
            'street' : location.street,
            'suite' : location.suite,
            'city' : location.city,
            'state' : location.state,
            'postal_code' : location.postal_code,
            'notes' : location.notes,
        }
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(input_json)
        )
        mocker.patch.object(
            Delivery_Location, 'save'
        )
        view = LocationsVewSet.as_view(
            {'post' : "create"}
        )
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

        response = view(request).render()

        assert response.status_code == 201
        valid_data_dict['created']['id'] = response.data['created']['id']
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf, new_location, prepare_location_dict):
        old_location = new_location
        location_dict = prepare_location_dict['location_dict']['created']
        
        url = reverse('locations-detail', args=[old_location.id])
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(location_dict)
        )
        mocker.patch.object(
            LocationsVewSet, 'get_object', return_value=old_location
        )
        mocker.patch.object(
            Delivery_Location, 'save'
        )
        view = LocationsVewSet.as_view(
            {'put' : 'update'}
        )

        response = view(request, pk=old_location.id).render()
        location_dict['id'] = response.data['id']

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
    def test_partial_update(self, mocker, rf, field, new_location, prepare_location_dict):
        old_location = new_location
        location_dict = prepare_location_dict['location_dict']['created']

        valid_data = location_dict[field]
        url = reverse('locations-detail', args=[old_location.id])
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: valid_data})
        )
        mocker.patch.object(
            LocationsVewSet, 'get_object', return_value=old_location
        )
        mocker.patch.object(
            Delivery_Location, 'save'
        )
        view = LocationsVewSet.as_view(
            {'patch' : 'partial_update'}
        )

        response = view(request, pk=old_location.id).render()

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_data

    def test_delete(self, mocker, rf, new_location):
        
        url = reverse('locations-detail', args=[new_location.id])
        request = rf.delete(url)
        mocker.patch.object(
            LocationsVewSet, 'get_object', return_value=new_location
        )
        del_mock = mocker.patch.object(
            Delivery_Location, 'delete'
        )
        view = LocationsVewSet.as_view(
            {'delete' : 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        assert del_mock.assert_called