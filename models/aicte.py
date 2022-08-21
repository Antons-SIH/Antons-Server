from db import db

class AicteModel(db.Model):
    __tablename__ = 'aicte'

    email = db.Column(db.String(80),primary_key=True)
    password = db.Column(db.String(150))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(20))
    user_type = db.Column(db.String(20))
    aadhar = db.Column(db.String(14))
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

    def __init__(self,email,password,phone,gender,user_type,aadhar,aadhar_remark,aadhar_date, seeded_bank_acc,seeded_remark,seeded_date,pan,pan_remark,pan_date,name,college,address,dob,admission_year):
        self.email=email
        self.password=password
        self.phone=phone
        self.gender = gender
        self.user_type=user_type
        self.aadhar = aadhar
        self.aadhar_remark=aadhar_remark
        self.aadhar_date=aadhar_date
        self.seeded_bank_acc = seeded_bank_acc
        self.pan = pan
        self.name = name
        self.college = college
        self.seeded_remark=seeded_remark
        self.seeded_date=seeded_date
        self.pan_remark=pan_remark
        self.pan_date=pan_date
        self.address=address
        self.dob=dob
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
