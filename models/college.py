from db import db

class CollegeModel(db.Model):
    __tablename__ = 'college'

    id = db.Column(db.String(100),unique=True)
    college = db.Column(db.String(100),primary_key=True)

    def __init__(self,id,college):
        self.id = id
        self.college = college

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_college(cls,college):
        return cls.query.filter_by(college=college)
    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id)
    
    @classmethod
    def find_all(cls):
        return cls.query.all()