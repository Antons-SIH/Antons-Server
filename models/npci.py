from db import db

class NpciModel(db.Model):
    __tablename__ = 'npci'

    aadhar = db.Column(db.String(14),primary_key=True)
    seeded_bank_acc = db.Column(db.String(30))
    
    def __init__(self, aadhar, seeded_bank_acc):
        self.aadhar = aadhar
        self.seeded_bank_acc = seeded_bank_acc
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_aadhar(cls, aadhar):
        return cls.query.filter_by(aadhar=aadhar).first()

