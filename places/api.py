from flask_restplus import Api, Resource, fields
from places.model import db, Places
from flask import jsonify

api = Api()

ns = api.namespace('places', description='The places of Seven Kingdoms')

place = api.model(
    'Place',
    {'name': fields.String(required=True, description='The place name')})


class PlaceDAO(object):
    def select(self, id):
        return Places.query.filter_by(id=id).first()

    def handle_duplicated(self, data):
        places_with_same_name = Places.query.filter_by(name=data['name']).all()
        if (len(places_with_same_name) > 0):
            ns.abort(
                400,
                f"There're already has a place with name {data['name']} (id: {places_with_same_name[0].id})"
            )

    def create(self, data):
        self.handle_duplicated(data)
        new_place = Places(name=data['name'])
        db.session.add(new_place)
        db.session.flush()
        db.session.commit()
        return new_place.id

    def read(self, id):
        place = self.select(id)
        if (place is not None):
            return jsonify(place.serializable)
        else:
            ns.abort(404, f"Place with ID {id} not found")

    def update(self, id, data):
        self.handle_duplicated(data)
        place = self.select(id)
        place.name = data['name']
        db.session.commit()

    def delete(self, id):
        place = self.select(id)
        db.session.delete(place)
        db.session.commit()


DAO = PlaceDAO()


@ns.route('/')
class PlacesList(Resource):
    '''Shows a list of all places, and lets you POST to add new places'''

    @ns.doc('list_places')
    def get(self):
        '''List all places'''
        places_list = Places.query.all()
        return jsonify([i.serializable for i in places_list])

    @ns.doc('create_place')
    @ns.response(201, 'Place created successfully')
    @ns.response(400, 'Bad request')
    @ns.expect(place)
    def post(self):
        '''Create a new place'''
        return f"Place created successfully with ID {DAO.create(api.payload)}", 201


@ns.route('/<int:id>')
@ns.response(404, 'Place not found')
@ns.param('id', 'The place unique identifier')
class SinglePlace(Resource):
    '''Show a single place item and lets you delete them'''

    @ns.doc('get_place')
    @ns.response(200, 'Success')
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.read(id)

    @ns.doc('delete_place')
    @ns.response(200, 'Place deleted')
    def delete(self, id):
        '''Delete a place given its identifier'''
        DAO.delete(id)
        return f"Place with ID {id} has been deleted", 200

    @ns.doc('update_place')
    @ns.response(200, 'Place updated')
    @ns.response(400, 'Bad request')
    @ns.expect(place)
    def put(self, id):
        '''Update a place given its identifier'''
        DAO.update(id, api.payload)
        return f"Place with ID {id} has been updated", 200
