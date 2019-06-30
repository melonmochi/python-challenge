from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String

db = SQLAlchemy()


#  Places Model
class Places(db.Model):
    __bind_key__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    @property
    def serializable(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return '<Place %r>' % self.name


#  People Model
class People(db.Model):
    __bind_key__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    isAlive = Column(Boolean, default=False, nullable=False)
    isKing = Column(Boolean, default=False)
    placeId = Column(Integer)

    @property
    def serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'isAlive': self.isAlive,
            'isKing': self.isKing,
            'placeId': self.placeId
        }

    def __repr__(self):
        return '<People %r>' % self.name
