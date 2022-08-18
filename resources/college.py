from flask_restful import (Resource, reqparse, request)
from util.response import HttpApiResponse, HttpErrorResponse
from models.college import CollegeModel
from sqlalchemy import null

class CollegeDetails(Resource):
    reg_parser = reqparse.RequestParser()
    reg_parser.add_argument('college', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('id', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data=CollegeDetails.reg_parser.parse_args()
        print(data['college'])
        # if CollegeModel.find_by_college(data['college']):
        #     return HttpErrorResponse({"message": "A college with that name already exists"}), 400

        saveCollege=CollegeModel(data['id'],data['college'])
        saveCollege.save_to_db()

        return HttpApiResponse({"message": "College created successfully."}), 201
    
    def get(self):
        colleges=CollegeModel.find_all()
        CollegeNames=[]
        for college in colleges:
            CollegeNames.append({
                "id":college.id,
                "college":college.college
            })
        return HttpApiResponse(CollegeNames),200