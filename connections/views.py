from http import HTTPStatus

from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.connection import Connection
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people/<int:id>/mutual_friends', methods=['GET'])
@use_args( {'target_id': fields.Int(required=True, location='query')} )
def get_mutual_friends(args, id):
    people_schema = PersonSchema(many=True)
    person = Person.query.get_or_404(id)
    target = Person.query.get_or_404(args['target_id'])
    return people_schema.jsonify(person.mutual_friends(target)), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<id>', methods=['PATCH'])
@use_args(ConnectionSchema(), locations=('json',))
def update_connection_type(dummy_connection, id):
    connection = Connection.query.get_or_404(id)
    connection.update(connection_type=dummy_connection.connection_type)
    return ConnectionSchema().jsonify(connection), HTTPStatus.OK
