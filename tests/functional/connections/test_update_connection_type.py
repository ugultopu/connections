from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory

from connections.models.connection import Connection


def test_can_update_connection_type(db, testapp):
    person_from = PersonFactory(first_name='Diana')
    person_to = PersonFactory(first_name='Harry')
    connection = ConnectionFactory(from_person=person_from,
                                   to_person=person_to,
                                   connection_type='mother')
    db.session.commit()
    person_from.reload()
    person_to.reload()

    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'mother'

    payload = {
        'connection_type': 'friend',
    }
    res = testapp.patch(f'/connections/{connection.id}', json=payload)

    assert res.status_code == HTTPStatus.OK

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == payload['connection_type']
