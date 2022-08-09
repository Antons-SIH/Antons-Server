from db import db

class PanModel(db.Model):
    __tablename__ = 'pan'

    pan = db.Column(db.String(14),primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)

    def __init__(self, pan, name, address,dob):
        self.pan = pan
        self.name = name
        self.address = address
        self.dob = dob

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_pan(cls, pan):
        return cls.query.filter_by(pan=pan).first()

