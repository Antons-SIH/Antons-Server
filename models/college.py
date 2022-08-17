from db import db

class CollegeModel(db.model):
    __tablename__ = 'college'
    id = db.Column(db.String(100),unique=True)
    college = db.Column(db.String(100),primary_key=True)

    @classmethod
    def find_by_college(cls,college):
        return cls.query.filter_by(college=college)
    
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id)