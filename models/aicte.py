from db import db

class AicteModel(db.Model):
    __tablename__ = 'aicte'

    email = db.Column(db.String(80))
    password = db.Column(db.String(150))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(20))
    user_type = db.Column(db.String(20))
    aadhar = db.Column(db.String(14),primary_key=True)
    aadhar_remark = db.Column(db.String(50), default='Upload Aadhar to verify')## Aadhar remark
    aadhar_date = db.Column(db.DateTime(timezone=True), default=None)
    seeded_bank_acc = db.Column(db.String(30))
    seeded_remark = db.Column(db.String(50), default='Upload Aadhar to verify')## Bank remark
    seeded_date = db.Column(db.DateTime(timezone=True), default=None)
    pan = db.Column(db.String(14))
    pan_remark = db.Column(db.String(50), default='Upload Pan to verify')   ## Pan remark
    pan_date = db.Column(db.DateTime(timezone=True), default=None)
    name = db.Column(db.String(100))
    college = db.Column(db.String(100))
    address=db.Column(db.String(100))
    dob = db.Column(db.DateTime(timezone=True), default=None)
    admission_year=db.Column(db.String(5))

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
