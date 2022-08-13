import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.user import UserModel
from  werkzeug.security import generate_password_hash, check_password_hash
from util.response import HttpApiResponse, HttpErrorResponse
# imports for PyJWT authentication
import jwt

JWT_SECRET="ANTONS"

class GetDetails(Resource):
    def adminLogin(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            payload=jwt.decode(token,JWT_SECRET)
            admin=UserModel.find_by_id(payload['user_id'])

            if(admin):
                users=UserModel.find_college_users(admin.college)
                UserDetails=[]
                for user in users:
                    UserDetails.append({
                        "id":user.id,
                        "email":user.email,
                        "college":user.college,
                        "name":user.name,
                        "user_type":user.user_type,
                        "phone":user.phone,
                        "aadhar":user.aadhar,
                        "aadhar_date":str(user.aadhar_date),
                        "pan":user.pan,
                        "pan_date":str(user.pan_date),
                        "seeded_bank_acc":user.seeded_bank_acc,
                        "seeded_date":str(user.seeded_date)
                    })
                return HttpApiResponse({"users":UserDetails}),200
            else:
                return HttpErrorResponse("User Not Found!"),404

        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def superadminLogin(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            payload=jwt.decode(token,JWT_SECRET)
            superadmin=UserModel.find_by_id(payload['user_id'])

            if(superadmin):
                users=UserModel.find_all()
                UserDetails=[]
                for user in users:
                    UserDetails.append({
                        "id":user.id,
                        "email":user.email,
                        "college":user.college,
                        "name":user.name,
                        "user_type":user.user_type,
                        "phone":user.phone,
                        "aadhar":user.aadhar,
                        "aadhar_date":str(user.aadhar_date),
                        "pan":user.pan,
                        "pan_date":str(user.pan_date),
                        "seeded_bank_acc":user.seeded_bank_acc,
                        "seeded_date":str(user.seeded_date)
                    })
                return HttpApiResponse({"users":UserDetails}),200
            else:
                return HttpErrorResponse("User Not Found!"),404
        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def get(self):
        url=request.url
        if "admin" in url:
            return self.adminLogin()
        if "super" in url:
            return self.superadminLogin()