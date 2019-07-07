from flask_restplus import Api, Resource
import requests

api = Api()

ns = api.namespace('got',
                   description="The all information (GOT) of Seven Kingdoms")


@ns.route('/')
class GotClass(Resource):
    '''Shows a list of all places and each place shows its all people'''

    def get_places(self):
        try:
            places = requests.get(f"http://localhost:8081/places")
            return places.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            ns.abort(
                500,
                f"Some problem happens in Places server (error: {e}), please make sure the Places server works"
            )

    def get_people(self):
        try:
            people = requests.get(f"http://localhost:8082/people")
            return people.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            ns.abort(
                500,
                f"Some problem happens in People server (error: {e}), please make sure the People server works"
            )

    def add_people(self, place, people_dict):
        try:
            place['people'] = people_dict[place['id']]
        except KeyError:
            place['people'] = []
        return place

    @ns.doc('list_people')
    @ns.response(200, 'Get GOT list successfully')
    def get(self):
        '''Get all places'''
        places = self.get_places()
        '''Get all places'''
        people = self.get_people()
        '''Merge both'''
        people_dict = {}
        people_with_place = [
            people for people in people if people['placeId'] is not None
        ]
        for p in people_with_place:
            p_id = p['placeId']
            for k, v in dict(p).items():
                if v is None or k == 'placeId':
                    del p[k]
            try:
                people_dict[p_id].append(p)
            except KeyError:
                people_dict[p_id] = [p]
        return [self.add_people(p, people_dict) for p in places]
