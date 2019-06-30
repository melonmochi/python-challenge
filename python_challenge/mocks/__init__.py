from utils.json import load_json
from python_challenge.model import Places, People

MOCKS_PATH = 'python_challenge/mocks'


def people(obj):
    return People(id=obj['id'],
                  isAlive=obj['isAlive'],
                  name=obj['name'],
                  placeId=obj['placeId'])


def place(obj):
    return Places(id=obj['id'], name=obj['name'])


def insert_seeds(db, fn, objs):
    for obj in objs:
        db.session.add(fn(obj))


def populate_mocks(db):
    '''
    Delete existed registers
    '''
    db.session.query(Places).delete()
    db.session.query(People).delete()
    '''
    Insert seed registers into tables
    '''
    places_objs = load_json(f"{MOCKS_PATH}/places.json")
    people_objs = load_json(f"{MOCKS_PATH}/people.json")
    insert_seeds(db, place, places_objs)
    insert_seeds(db, people, people_objs)
    db.session.commit()
