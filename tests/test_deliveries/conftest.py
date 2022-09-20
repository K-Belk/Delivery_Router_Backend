import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from deliveries.models import Delivery_Location, Deliveries, EditionChoices, ProductChoices



@pytest.fixture
def api_client():
    return APIClient

@pytest.fixture
def new_location():
    return baker.make(Delivery_Location)

@pytest.fixture
def prepared_location():
    return baker.prepare(Delivery_Location)

@pytest.fixture
def new_location_dict(new_location):
    location = new_location
    return {
            'location' : location,
            'location_dict' : {
                'id' : location.id,
                'name' : location.name,
                'street' : location.street,
                'suite' : location.suite,
                'city' : location.city,
                'state' : location.state,
                'postal_code' : location.postal_code,
                'notes' : location.notes,
                'latitude' : location.latitude,
                'longitude' : location.longitude,
                'phone' : location.phone,
                'hours' : location.hours,
            }
        }

@pytest.fixture
def prepared_location_dict(prepared_location):
    location = prepared_location
    return {
        'location' : location,
        'expected_json' : {
            'created': {
                'name' : location.name,
                'street' : location.street,
                'suite' : location.suite,
                'city' : location.city,
                'state' : location.state,
                'postal_code' : location.postal_code,
                'notes' : location.notes,
                'latitude' : location.latitude,
                'longitude' : location.longitude,
                'phone' : location.phone,
                'hours' : location.hours,
        }}
    }

@pytest.fixture
def new_edition():
    return baker.make(EditionChoices)

@pytest.fixture
def prepare_edition():
    return baker.prepare(EditionChoices, year = 2013,_save_related=True)

@pytest.fixture
def new_edition_dict(new_edition):
    edition = new_edition
    return {
        'edition' : edition,
        'edition_dict' : {
            'id' : edition.id,
            'edition' : edition.edition,
            'year' : edition.year,
            'product' : edition.product.id
        }
    }

@pytest.fixture
def prepare_edition_dict(prepare_edition):
    edition = prepare_edition
    return {
        'edition' : edition,
        'edition_dict' : {
            'edition': edition.edition,
            'year' : edition.year,
            'product' : edition.product.id
        }
    }


@pytest.fixture
def new_delivery():
    return baker.make(Deliveries)

@pytest.fixture
def prepare_delivery():
    return baker.prepare(Deliveries,_save_related=True)

@pytest.fixture
def new_delivery_dict(new_delivery):
    delivery = new_delivery
    return {
        'delivery' : delivery,
        'delivery_dict' : {
            'id' : delivery.id,
            'driver' : delivery.driver.id,
            'edition' : delivery.edition.id,
            'product' : delivery.product.id,
            'amount' : delivery.amount,
            'date' : delivery.date,
            'location' : delivery.location.id
        },
        'delivery_response' : {
            'id' : delivery.id,
            'driver' : delivery.driver.first_name + ' ' + delivery.driver.last_name,
            'edition' : f"{delivery.edition.edition} {delivery.edition.year} {delivery.edition.product}",
            'product' : delivery.product.product,
            'amount' : delivery.amount,
            'date' : delivery.date,
            'location' : {
                'name' : delivery.location.name,
                'street' : delivery.location.street,
                'suite' : delivery.location.suite,
                'city' : delivery.location.city,
                'state' : delivery.location.state,
                'postal_code' : delivery.location.postal_code,
            }
        }
    }

@pytest.fixture
def prepare_delivery_dict(prepare_delivery):
    delivery = prepare_delivery
    return {
        'delivery' : delivery,
        'delivery_dict' : {
            'driver' : delivery.driver.id,
            'edition' : delivery.edition.id,
            'product' : delivery.product.id,
            'amount' : delivery.amount,
            'date' : delivery.date,
            'location' : delivery.location.id
        },
        'delivery_response' : {
            'driver' : delivery.driver.first_name + ' ' + delivery.driver.last_name,
            'edition' : f"{delivery.edition.edition} {delivery.edition.year} {delivery.edition.product}",
            'product' : delivery.product.product,
            'amount' : delivery.amount,
            'date' : delivery.date,
            'location' : {
                'name' : delivery.location.name,
                'street' : delivery.location.street,
                'suite' : delivery.location.suite,
                'city' : delivery.location.city,
                'state' : delivery.location.state,
                'postal_code' : delivery.location.postal_code,
            }
        }
    }