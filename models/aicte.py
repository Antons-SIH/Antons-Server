from enum import unique
from pickle import TRUE
from db import db
from util.time import nowTime
class AicteModel(db.Model):
    __tablename__ = 'aicte'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(150))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(20))
    user_type = db.Column(db.String(20))
    aadhar = db.Column(db.String(14))
    aadhar_remark = db.Column(db.String(50), default='Upload Aadhar to verify')## Aadhar remark
    seeded_bank_acc = db.Column(db.String(30))
    seeded_remark = db.Column(db.String(50), default='Upload Aadhar to verify')## Bank remark
    pan = db.Column(db.String(14))
    pan_remark = db.Column(db.String(50), default='Upload Pan to verify')   ## Pan remark
    name = db.Column(db.String(100))
    college = db.Column(db.String(100))
    address=db.Column(db.String(100))
    dob = db.Column(db.DateTime(timezone=True), default=None)
    admission_year=db.Column(db.String(10))
    last_updated=db.Column(db.DateTime(timezone=True), default=nowTime())

    def __init__(self,email,password,phone,gender,user_type,name,college,admission_year):
        self.email=email
        self.password=password
        self.phone=phone
        self.gender = gender
        self.user_type=user_type
        self.name = name
        self.college = college
        self.admission_year=admission_year

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_aadhar(cls, aadhar):
        return cls.query.filter_by(aadhar=aadhar).first()

    @classmethod
    def find_by_pan(cls, pan):
        return cls.query.filter_by(pan=pan).first()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod 
    def find_college_users(cls,college):
        return cls.query.filter_by(college=college)

    @classmethod
    def find_all(cls):
        return cls.query.all()