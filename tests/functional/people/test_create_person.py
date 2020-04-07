from http import HTTPStatus

import pytest

from connections.models.person import Person


@pytest.fixture
def person_payload():
    return {
        'first_name': 'Bob',
        'last_name': 'Loblaw',
        'email': 'bob.loblaw@lawblog.co',
    }


def test_can_create_person(db, testapp, person_payload):
    res = testapp.post('/people', json=person_payload)

    assert res.status_code == HTTPStatus.CREATED

    for field in person_payload:
        assert res.json[field] == person_payload[field]
    assert 'id' in res.json

    person = Person.query.get(res.json['id'])

    assert person is not None
    for field in person_payload:
        assert getattr(person, field) == person_payload[field]


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('first_name', None, 'Field may not be null.', id='missing first name'),
    pytest.param('email', None, 'Field may not be null.', id='missing email'),
    pytest.param('email', 'foo@bar', 'Not a valid email address.', id='invalid email'),
])
def test_create_person_validations(db, testapp, person_payload, field, value, error_message):
    person_payload[field] = value

    res = testapp.post('/people', json=person_payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]
