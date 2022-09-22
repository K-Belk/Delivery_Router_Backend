import pytest
import json
from model_bakery import baker
from django.urls import reverse
from django_mock_queries.query import MockSet
from deliveries.models import EditionChoices
from deliveries.views import EditionViewSet

pytestmark = pytest.mark.unit

class TestEditionViewset:

    def test_list(self, mocker, rf, db):
        url = reverse('edition-list')
        request = rf.get(url)
        qs = MockSet(
            baker.make(EditionChoices),
            baker.make(EditionChoices),
            baker.make(EditionChoices),
        )
        view = EditionViewSet.as_view(
            {'get' : 'list'}
        )

        mocker.patch.object(
            EditionViewSet, 'get_queryset', return_value=qs
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf, new_edition_dict):
        url = reverse('edition-detail', args=[new_edition_dict['edition'].id])
        expected_json = new_edition_dict['edition_dict']
        request = rf.get(url)
        mocker.patch.object(
            EditionViewSet, 'get_queryset', return_value=MockSet(new_edition_dict['edition'])
        )
        view = EditionViewSet.as_view(
            {'get' : 'retrieve' }
        )

        response = view(request, pk=new_edition_dict['edition'].id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_create(self, mocker, rf, prepare_edition_dict):
        url = reverse('edition-list')
        valid_data_dict = prepare_edition_dict['edition_dict']
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(prepare_edition_dict['edition_dict'])
        )
        mocker.patch.object(
            EditionChoices, 'save'
        )
        view = EditionViewSet.as_view(
            {'post' : "create"}
        )

        response = view(request).render()

        valid_data_dict['id'] = response.data['id']
        assert response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf, new_edition, prepare_edition_dict):
        old_edition = new_edition
        edition_dict = prepare_edition_dict['edition_dict']
        
        url = reverse('edition-detail', args=[old_edition.id])
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(edition_dict)
        )
        mocker.patch.object(
            EditionViewSet, 'get_object', return_value=old_edition
        )
        mocker.patch.object(
            EditionChoices, 'save'
        )
        view = EditionViewSet.as_view(
            {'put' : 'update'}
        )

        response = view(request, pk=old_edition.id).render()
        edition_dict['id'] = response.data['id']

        assert response.status_code == 200
        assert json.loads(response.content) == edition_dict

    @pytest.mark.parametrize('field', [
        ("edition"),
        ("year"),
        ("product")
    ])
    def test_partial_update(self, mocker, rf, field, new_edition, prepare_edition_dict):
        old_edition = new_edition
        edition_dict = prepare_edition_dict['edition_dict']

        valid_data = edition_dict[field]
        url = reverse('edition-detail', args=[old_edition.id])
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: valid_data})
        )
        mocker.patch.object(
            EditionViewSet, 'get_object', return_value=old_edition
        )
        mocker.patch.object(
            EditionChoices, 'save'
        )
        view = EditionViewSet.as_view(
            {'patch' : 'partial_update'}
        )

        response = view(request, pk=old_edition.id).render()

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_data

    def test_delete(self, mocker, rf, new_edition):
        
        url = reverse('edition-detail', args=[new_edition.id])
        request = rf.delete(url)
        mocker.patch.object(
            EditionViewSet, 'get_object', return_value=new_edition
        )
        del_mock = mocker.patch.object(
            EditionChoices, 'delete'
        )
        view = EditionViewSet.as_view(
            {'delete' : 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        assert del_mock.assert_called