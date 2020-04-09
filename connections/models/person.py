from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.connection import ConnectionType


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, other_person):
        other_person_friends = [c.to_person for c in other_person.connections if c.connection_type is ConnectionType.friend]
        my_friends = [c.to_person for c in self.connections if c.connection_type is ConnectionType.friend]
        return [f for f in my_friends if f in other_person_friends]
