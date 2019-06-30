from flask_restplus import Api, Resource, reqparse
from python_challenge.model import db, People, Places
from flask import json, jsonify, request

api = Api()

people_name_space = api.namespace('people', description="im people")
places_name_space = api.namespace('places', description="im places")
got_name_space = api.namespace('got', description="im got")
'''
PEOPLE
'''

post_dic = {
    'name': 'name',
    'isAlive': 'isAlive',
    'isKing': 'isKing',
    'placeId': 'placeId'
}


@people_name_space.route('/')
class PeopleClass(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Error'})
    def get(self):
        try:
            people_list = db.session.query(People)
            return jsonify([i.serializable for i in people_list])
        except Exception as e:
            abort_500(people_name_space, e)

    # @api.doc(responses={201: 'OK', 500: 'Internal Error'}, params=post_dic)
    # def post(self):
    #     try:
    #         name, isAlive, isKing, placeId = request.args.get(
    #             'name'), request.args.get('isAlive'), request.args.get(
    #                 'isKing'), request.args.get('placeId')
    #         parser = reqparse.RequestParser()
    #         parser.add_argument(name,
    #                             type=str,
    #                             help='name cannot be converted')
    #         print(parser.parse_args())
    #         if (isAlive is None):
    #             isAlive = 'false'
    #         if (placeId is None) and (isAlive is True):
    #             return 'Any alived people need to be set a place where belong', 400
    #         if (len(db.session.query(Places).filter_by(
    #                 id=placeId).all()) == 0):
    #             return f"placeId {placeId} not found", 400
    #         if (len(
    #                 db.session.query(People).filter_by(
    #                     isKing=True, placeId=placeId, isAlive=isAlive).all()) >
    #                 0):
    #             return f"placeId {placeId} only accept one king", 400
    #         new_people = People(name=name,
    #                             isAlive=isAlive,
    #                             isKing=isKing,
    #                             placeId=placeId)
    #         db.session.add(new_people)
    #         db.session.commit()
    #         return 201
    #     except Exception as e:
    #         abort_500(places_name_space, e)


@people_name_space.route('/<int:id>')
class OnePeopleClass(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Error'}, params={'id': 'id'})
    def get(self, id):
        try:
            people = db.session.query(People).filter_by(id=id).first()
            return jsonify(people.serializable)
        except Exception as e:
            abort_500(people_name_space, e)


'''
PLACES
'''


@places_name_space.route('/')
class PlacesClass(Resource):
    @api.doc({200: 'OK', 500: 'Internal Error'})
    def get(self):
        try:
            places_list = db.session.query(Places)
            return jsonify([i.serializable for i in places_list])
        except Exception as e:
            abort_500(places_name_space, e)

    @api.doc(responses={
        201: 'OK',
        500: 'Internal Error'
    },
             params={
                 'id': 'id',
                 'name': 'name'
             })
    def post(self):
        try:
            id, name = request.args.get('id'), request.args.get('name')
            new_place = Places(id=id, name=name)
            db.session.add(new_place)
            db.session.commit()
            return 201
        except Exception as e:
            abort_500(places_name_space, e)

    @api.doc(responses={
        201: 'OK',
        500: 'Internal Error'
    },
             params={
                 'id': 'id',
                 'name': 'name'
             })
    def put(self):
        try:
            id, name = request.args.get('id'), request.args.get('name')
            place = db.session.query(Places).filter_by(id=id).first()
            place.name = name
            db.session.commit()
            return 201
        except Exception as e:
            abort_500(places_name_space, e)


@places_name_space.route('/<int:id>')
class OnePlaceClass(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Error'}, params={'id': 'id'})
    def get(self, id):
        try:
            place = db.session.query(Places).filter_by(id=id).first()
            return jsonify(place.serializable)
        except Exception as e:
            abort_500(places_name_space, e)


'''
GOT
'''


@got_name_space.route('/')
class GotClass(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Error'})
    def get(self):
        try:
            places_list = db.session.query(Places)
            list = []
            for place in places_list:
                place_id = place.id
                people_list = db.session.query(People).filter_by(
                    placeId=place_id).all()
                people_objs = data_2_json(
                    [i.serializable for i in people_list])
                place_obj = data_2_json(place.serializable)
                place_obj['people'] = people_objs
                list.append(place_obj)
            return list
        except Exception as e:
            abort_500(people_name_space, e)


def abort_500(namespace, e):
    namespace.abort(500,
                    e.__doc__,
                    status="Could not retrieve information",
                    statusCode="500")


def data_2_json(data):
    return json.loads(jsonify(data).data)
