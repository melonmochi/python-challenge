from utils.json import load_json
from utils.insert_seeds import insert_seeds
from people.model import People


def people(obj):
    return People(id=obj['id'],
                  isAlive=obj['isAlive'],
                  name=obj['name'],
                  placeId=obj['placeId'])


def populate_mocks(db):
    db.session.query(People).delete()
    people_objs = load_json('people/mocks/plapeopleces.json')
    insert_seeds(db, people, people_objs)
    db.session.commit()
