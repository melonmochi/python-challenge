from utils.json import load_json
from utils.insert_seeds import insert_seeds
from places.model import Places


def place(obj):
    return Places(id=obj['id'], name=obj['name'])


def populate_mocks(db):
    db.session.query(Places).delete()
    places_objs = load_json('places/mocks/places.json')
    insert_seeds(db, place, places_objs)
    db.session.commit()
