from db import db
from util.time import nowTime

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=nowTime())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=nowTime(), server_onupdate=nowTime())
    email = db.Column(db.String(80))
    password = db.Column(db.String(150))
    college = db.Column(db.String(100))
    name = db.Column(db.String(100))
    user_type = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    aadhar = db.Column(db.String(14), default=None)                   ## Aadhar No.
    aadhar_date = db.Column(db.DateTime(timezone=True), default=None) ## Last verified aadhar details
    pan = db.Column(db.String(14), default=None)                      ## Pan No.
    pan_date = db.Column(db.DateTime(timezone=True), default=None)    ## Last verified pan details
    seeded_bank_acc = db.Column(db.String(30), default=None)          ## Bank No.
    seeded_date = db.Column(db.DateTime(timezone=True), default=None) ## Last verified bank details

    def __init__(self, email, password,college,name,user_type,phone):
        self.email = email
        self.password = password
        self.college = college
        self.name = name
        self.user_type = user_type
        self.phone = phone

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()