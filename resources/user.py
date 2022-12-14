import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.aicte import AicteModel
from  werkzeug.security import generate_password_hash, check_password_hash
from util.response import HttpApiResponse, HttpErrorResponse
from util.jwt import createToken,decodeToken
import random, math, requests,os

class Authentication(Resource):
    reg_parser = reqparse.RequestParser()
    reg_parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('college', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('first_name', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('last_name',type=str,required=True, help="This field cannot be blank.")
    reg_parser.add_argument('user_type', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('phone',type=str,required=True, help="This field cannot be blank.")
    reg_parser.add_argument('admission_year',type=str,required=True, help="This field cannot be blank.")
    reg_parser.add_argument('gender',type=str,required=True, help="This field cannot be blank.")

    log_parser = reqparse.RequestParser()
    log_parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")
    log_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    verify_parser = reqparse.RequestParser()
    verify_parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")
    verify_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    verify_parser.add_argument('otp', type=str, required=True, help="This field cannot be blank.")

    def register(self):
        data = Authentication.reg_parser.parse_args()

        if AicteModel.find_by_email(data['email']):
            return HttpErrorResponse({"message": "A user with that email already exists"}), 400
        
        password=generate_password_hash(data['password'])
        name=data['first_name']+" "+data['last_name']
        user = AicteModel(data['email'], password,data['phone'],data['gender'],data['user_type'],name, data['college'], data['admission_year'])
        user.save_to_db()

        return HttpApiResponse({"message": "User created successfully."}), 201

    def login(self):
        data = Authentication.log_parser.parse_args()
        user=AicteModel.find_by_email(data['email'])
        if not user:
            return HttpErrorResponse({"message": "User does not exist"}), 401

        if check_password_hash(user.password, data['password']):

            ## Generate OTP
            digits = [i for i in range(0, 10)]
            otp = ""

            for i in range(6):
                index = math.floor(random.random() * 10)
                otp += str(digits[index])

            user.otp = otp
            user.save_to_db()

            postDict={'email':data['email'], 'msg':"Your OTP for login at AICTE portal is: " + otp}
            requests.post(os.getenv("EMAIL_URL"),json=postDict)

            return HttpApiResponse({"email": user.email,"user_type": user.user_type, "college": user.college,"message":"token sent"}), 201
        
        return HttpErrorResponse({"message":"invalid password"}), 403


    def VerifyOtp(self):
        data = Authentication.verify_parser.parse_args()
        email = data['email']
        password = data['password']
        otp = data['otp']
        user=AicteModel.find_by_email(email)

        if not user:
            return HttpErrorResponse({"message": "User does not exist"}), 401

        if user.otp == otp:
            token=createToken(user.id)
            return HttpApiResponse({"token":token.decode('UTF-8'), "email": user.email,"user_type": user.user_type, "college": user.college,"message":"token sent"}), 201 
        
        return HttpErrorResponse({"message":"invalid otp"}), 403

    def profile(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            user=AicteModel.find_by_id(id)
            if(user):
                aadharIndexes = [0,1,2,3,4,5,6,7]
                panIndexes = [0,1,2,3,4,5]
                new_character = 'X' 
                aadhar=user.aadhar
                pan=user.pan
                if(aadhar):
                    for i in aadharIndexes:
                        aadhar = aadhar[:i] + new_character + aadhar[i+1:]
                if(pan):
                    for i in panIndexes:
                        pan = pan[:i] + new_character + pan[i+1:]

                return HttpApiResponse({"id":user.id,"email":user.email,"college":user.college,"name":user.name,"user_type":user.user_type,"phone":user.phone,"aadhar":aadhar, "aadhar_remark": user.aadhar_remark,"pan":pan, "pan_remark":user.pan_remark, "seeded_bank_acc":user.seeded_bank_acc,"seeded_remark": user.seeded_remark,"dob":str(user.dob),"gender":user.gender,"last_updated":str(user.last_updated)}), 200
                
            else:
                return HttpErrorResponse("Information denied, no authentication!"),404

        else:
            return HttpErrorResponse("Token Not found! Secured route access denied!"),404

    def post(self):
        url = request.url
        if "login" in url:
            return self.login()
        elif "register" in url:
            return self.register()
        elif "verify" in url:
            return self.VerifyOtp()

    def get(self):
        url = request.url
        if "profile" in url:
            return self.profile()
