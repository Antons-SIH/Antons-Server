import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.aicte import AicteModel
from werkzeug.security import generate_password_hash, check_password_hash
from util.response import HttpApiResponse, HttpErrorResponse
from util.jwt import createToken,decodeToken

class GetDetails(Resource):
    def adminLogin(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            findUser=AicteModel.find_by_id(id)

            if(findUser.user_type=="Admin"):
                users=AicteModel.find_college_users(findUser.college)
                UserDetails=[]
                for user in users:
                    if user.user_type=="Student" or user.user_type=="Teacher":
                        UserDetails.append({
                            "id":user.id,
                            "email":user.email,
                            "college":user.college,
                            "name":user.name,
                            "dob":user.dob,
                            "admission_year": user.admission_year,
                            "address": user.address,
                            "user_type":user.user_type,
                            "phone":user.phone,
                            "aadhar":user.aadhar,
                            "aadhar_remark":user.aadhar_remark,
                            "pan":user.pan,
                            "pan_remark":user.pan_remark,
                            "seeded_bank_acc":user.seeded_bank_acc,
                            "seeded_remark": user.seeded_remark,
                            "last_updated": str(user.last_updated)
                        })
                return HttpApiResponse(UserDetails),200
            else:
                return HttpErrorResponse("Details cannot be fetched. User not authorised!"),404
        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def superadminLogin(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            findUser=AicteModel.find_by_id(id)

            if(findUser.user_type=="Super"):
                users=AicteModel.find_all()
                UserDetails=[]
                for user in users:
                    if user.user_type=="Student" or user.user_type=="Teacher":
                        UserDetails.append({
                            "id":user.id,
                            "email":user.email,
                            "college":user.college,
                            "name":user.name,
                            "dob":user.dob,
                            "admission_year": user.admission_year,
                            "user_type":user.user_type,
                            "phone":user.phone,
                            "aadhar":user.aadhar,
                            "aadhar_remark":user.aadhar_remark,
                            "pan":user.pan,
                            "pan_remark":user.pan_remark,
                            "seeded_bank_acc":user.seeded_bank_acc,
                            "seeded_remark": user.seeded_remark,
                            "last_updated": str(user.last_updated)
                        })
                return HttpApiResponse(UserDetails),200
            else:
                return HttpErrorResponse("Details cannot be fetched. User not authorised!"),404
        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def get(self):
        url=request.url
        if "admin" in url:
            return self.adminLogin()
        if "super" in url:
            return self.superadminLogin()