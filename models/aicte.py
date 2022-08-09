from db import db

class AicteModel(db.Model):
    __tablename__ = 'aicte'

    aadhar = db.Column(db.String(14),primary_key=True)
    seeded_bank_acc = db.Column(db.String(30))
    pan = db.Column(db.String(14))
    name = db.Column(db.String(100))
    college = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    
    def __init__(self, aadhar, seeded_bank_acc,pan,name,college,gender):
        self.aadhar = aadhar
        self.seeded_bank_acc = seeded_bank_acc
        self.pan = pan
        self.name = name
        self.college = college
        self.gender = gender

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_aadhar(cls, aadhar):
        return cls.query.filter_by(aadhar=aadhar).first()

    @classmethod
    def find_by_pan(cls, pan):
        return cls.query.filter_by(pan=pan).first()
