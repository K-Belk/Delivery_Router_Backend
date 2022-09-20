import json
import pytest
from model_bakery import baker
from django.urls import reverse
from deliveries.models import EditionChoices

pytestmark = pytest.mark.django_db

class TestEditionChoicesEndpoints:

    endpoint = reverse('edition-list')

    def test_list(self, api_client):
        baker.make(EditionChoices, _quantity=3)

        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client, prepare_edition_dict):
        input_json = prepare_edition_dict['edition_dict']
        expected_json = prepare_edition_dict['edition_dict']
        response = api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
        )
        assert response.status_code == 201
        expected_json['id'] = response.data['id']
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field',[
        ("edition"),
        ("year"),
        ("product")
    ])
    def test_invalid_create(self, api_client, field, prepare_edition_dict):
        input_json = prepare_edition_dict['edition_dict']
        input_json[field] = ''

        response =api_client().post(
            self.endpoint,
            data=input_json,
            format='json'
            )
        assert response.status_code == 400

    def test_retrieve(self, api_client, new_edition_dict):

        edition = new_edition_dict['edition']
        expected_json = new_edition_dict['edition_dict']
        url = f'{self.endpoint}{edition.id}/'
        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, new_edition, prepare_edition_dict):

        old_edition = new_edition
        edition_dict = prepare_edition_dict['edition_dict']
        edition_dict['id'] = old_edition.id
        url = f'{self.endpoint}{old_edition.id}/'
        response = api_client().put(url, edition_dict, format='json')
        assert response.status_code == 200
        assert json.loads(response.content) == edition_dict

    @pytest.mark.parametrize('field', [
        ("edition"),
        ("year"),
        ("product")
    ])
    def test_partial_update(self, field, api_client, prepare_edition_dict):
        old_edition = baker.make(EditionChoices)
        edition_dict = prepare_edition_dict['edition_dict']

        valid_data = edition_dict[field]
        url = f'{self.endpoint}{old_edition.id}/'
        response = api_client().patch(url, {field: valid_data}, format='json')

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_data

    def test_delete(self, api_client):

        edition = baker.make(EditionChoices)
        url = f'{self.endpoint}{edition.id}/'
        response = api_client().delete(url)
        assert response.status_code == 204
        assert EditionChoices.objects.all().count() == 0