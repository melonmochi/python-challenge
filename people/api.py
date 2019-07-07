from flask_restplus import Api, Resource, fields
from people.model import db, People
from flask import jsonify
import requests

api = Api()

ns = api.namespace('people', description="The people of Seven Kingdoms")

people = api.model(
    'People', {
        'name':
        fields.String(required=True, description="People's name"),
        'isAlive':
        fields.Boolean(required=False,
                       default=False,
                       description="People's alive status"),
        'isKing':
        fields.Boolean(
            required=False, default=False, description="If People is king"),
        'placeId':
        fields.Integer(
            description="The placeID of the place where the people belongs")
    })


class PeopleDAO(object):
    def select(self, id):
        return People.query.filter_by(id=id).first()

    def validate_name(self, id, data):
        self.check_duplicated_name(
            id, data['name']) if 'name' in data else ns.abort(
                400, "Field 'name' is required")

    def check_duplicated_name(self, id, name):
        other_names = People.query.filter_by(name=name).filter(
            People.id != id).all()
        if (len(other_names) > 0):
            ns.abort(
                400,
                f"There're already has a people with name {name} (id: {other_names[0].id})"
            )

    def validate_isAlive(self, data):
        if 'isAlive' not in data:
            data['isAlive'] = False

    def validate_placeId(self, data):
        if data['isAlive'] is True:
            (self.check_place_exists(data['placeId'])
             if 'placeId' in data else ns.abort(
                 400,
                 'Any alived people need have a place (placeId field is None)')
             )

    def validate_isKing(self, id, data):
        if 'isKing' not in data:
            data['isKing'] = False
        if data['isKing'] is True and data['isAlive'] is True:
            self.check_doble_kings(id, data['placeId'])

    def check_doble_kings(self, id, placeId):
        other_kings = People.query.filter_by(
            placeId=placeId, isAlive=True,
            isKing=True).filter(People.id != id).all()
        if (len(other_kings) > 0):
            ns.abort(
                400,
                f"There're already has a king (id: {other_kings[0].id}) in the place (id: {placeId})"
            )

    def check_place_exists(self, placeId):
        try:
            place = requests.get(f"http://localhost:8081/places/{placeId}")
            if (place.status_code == 404):
                ns.abort(
                    400,
                    f"The place where belongs the people (placeId: {placeId}) not exists"
                )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            ns.abort(
                500,
                f"Some problem happens in Places server (error: {e}), please make sure the Places server works"
            )

    def validate_data(self, id, data):
        '''name'''
        self.validate_name(id, data)
        '''isAlive'''
        self.validate_isAlive(data)
        '''placeId'''
        self.validate_placeId(data)
        '''isKing'''
        self.validate_isKing(id, data)

    def create(self, data):
        self.validate_data(None, data)
        new_people = People(**data)
        db.session.add(new_people)
        db.session.flush()
        db.session.commit()
        return new_people.id

    def read(self, id):
        people = self.select(id)
        if (people is not None):
            return jsonify(people.serializable)
        else:
            ns.abort(404, f"People with ID {id} not found")

    def update(self, id, data):
        self.validate_data(id, data)
        people = self.select(id)
        people.name = data['name']
        people.isAlive = data['isAlive']
        people.isKing = data['isKing']
        if 'placeId' in data:
            people.placeId = data['placeId']
        db.session.commit()

    def delete(self, id):
        people = self.select(id)
        db.session.delete(people)
        db.session.commit()


DAO = PeopleDAO()


@ns.route('/')
class PeopleList(Resource):
    '''Shows a list of all people, and lets you POST to add new people'''

    @ns.doc('list_people')
    def get(self):
        '''List all people'''
        people_list = People.query.all()
        return jsonify([i.serializable for i in people_list])

    @ns.doc('create_people')
    @ns.response(201, 'People created successfully')
    @ns.response(400, 'Bad request')
    @ns.expect(people)
    def post(self):
        '''Create a new people'''
        return f"People created successfully with ID {DAO.create(api.payload)}", 201


@ns.route('/<int:id>')
@ns.response(404, 'People not found')
@ns.param('id', 'The people unique identifier')
class SinglePeople(Resource):
    '''Show a single people item and lets you delete them'''

    @ns.doc('get_people')
    @ns.response(200, 'Success')
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.read(id)

    @ns.doc('delete_people')
    @ns.response(200, 'People deleted')
    def delete(self, id):
        '''Delete a people given its identifier'''
        DAO.delete(id)
        return f"People with ID {id} has been deleted", 200

    @ns.doc('update_people')
    @ns.response(200, 'People updated')
    @ns.response(400, 'Bad request')
    @ns.expect(people)
    def put(self, id):
        '''Update a place given its identifier'''
        DAO.update(id, api.payload)
        return f"People with ID {id} has been updated", 200
