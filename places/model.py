from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


#  Places Model
class Places(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    @property
    def serializable(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return '<Place %r>' % self.name
