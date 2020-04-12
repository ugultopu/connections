from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory


def mutual_friends_test_helper(instance_id, target_id, expected_mutual_friend_ids, testapp):
    mutual_friends_result = testapp.get(
        f'/people/{instance_id}/mutual_friends?target_id={target_id}'
    )

    assert mutual_friends_result.status_code == HTTPStatus.OK

    results = mutual_friends_result.json

    assert len(results) == 3
    for person in results:
        assert person['id'] in expected_mutual_friend_ids

    return results


def test_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    instance_to_target_mutual_friends = mutual_friends_test_helper(
                                            instance.id,
                                            target.id,
                                            expected_mutual_friend_ids,
                                            testapp
                                        )

    target_to_instance_mutual_friends = mutual_friends_test_helper(
                                            target.id,
                                            instance.id,
                                            expected_mutual_friend_ids,
                                            testapp
                                        )

    assert instance_to_target_mutual_friends == target_to_instance_mutual_friends
