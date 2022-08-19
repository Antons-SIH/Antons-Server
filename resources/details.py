import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from util.response import HttpApiResponse, HttpErrorResponse
from util.jwt import createToken,decodeToken

class GetDetails(Resource):
    def adminLogin(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            findUser=UserModel.find_by_id(id)

            if(findUser.user_type=="Admin"):
                users=UserModel.find_college_users(findUser.college)
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
                        "aadhar_remark":user.aadhar_remark,
                        "aadhar_date":str(user.aadhar_date),
                        "pan":user.pan,
                        "pan_remark":user.pan_remark,
                        "pan_date":str(user.pan_date),
                        "seeded_bank_acc":user.seeded_bank_acc,
                        "seeded_remark": user.seeded_remark,
                        "seeded_date":str(user.seeded_date)
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
            findUser=UserModel.find_by_id(id)

            if(findUser.user_type=="Super"):
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
                        "aadhar_remark":user.aadhar_remark,
                        "aadhar_date":str(user.aadhar_date),
                        "pan":user.pan,
                        "pan_remark":user.pan_remark,
                        "pan_date":str(user.pan_date),
                        "seeded_bank_acc":user.seeded_bank_acc,
                        "seeded_remark": user.seeded_remark,
                        "seeded_date":str(user.seeded_date)
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