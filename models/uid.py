from db import db

class UidModel(db.Model):
    __tablename__ = 'uid'

    aadhar = db.Column(db.String(14),primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    phone = db.Column(db.String(15))

    def __init__(self, aadhar, name,gender,address,dob,phone):
        self.aadhar = aadhar
        self.name = name
        self.gender = gender
        self.address = address
        self.dob = dob
        self.phone=phone
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_aadhar(cls, aadhar):
        return cls.query.filter_by(aadhar=aadhar).first()

