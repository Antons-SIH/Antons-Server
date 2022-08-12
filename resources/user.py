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

class Authentication(Resource):
    reg_parser = reqparse.RequestParser()
    reg_parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('college', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('first_name', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('last_name',type=str,required=True, help="This field cannot be blank.")
    reg_parser.add_argument('user_type', type=str, required=True, help="This field cannot be blank.")
    reg_parser.add_argument('phone',type=str,required=True, help="This field cannot be blank.")

    log_parser = reqparse.RequestParser()
    log_parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")
    log_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def register(self):
        data = Authentication.reg_parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        
        password=generate_password_hash(data['password'])
        name=data['first_name']+" "+data['last_name']
        user = UserModel(data['email'], password, data['college'], name, data['user_type'], data['phone'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

    def login(self):
        data = Authentication.log_parser.parse_args()

        user=UserModel.find_by_email(data['email'])
        print(user)
        if not user:
            return {"message": "User does not exist"}, 401

        if check_password_hash(user.password, data['password']):
            # generates the JWT Token
            token = jwt.encode({
            'user_id': user.id
            # 'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, JWT_SECRET)

            return ({"token":token.decode('UTF-8'), "email": user.email,"user_type": user.user_type, "college": user.college,"message":"token sent"},201)
        
        return ({"message":"invalid password"},403)

    def profile(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            payload=jwt.decode(token,JWT_SECRET)
            # print(payload['user_id'])
            user=UserModel.find_by_id(payload['user_id'])
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
            # userDetails=json.dumps({"id":user.id,"email":user.email,"college":user.college,"name":user.name,"user_type":user.user_type,"phone":user.phone,"aadhar":aadhar,"aadhar_date":str(user.aadhar_date),"pan":pan,"pan_date":str(user.pan_date)}, default=str)
            
            return HttpApiResponse({"id":user.id,"email":user.email,"college":user.college,"name":user.name,"user_type":user.user_type,"phone":user.phone,"aadhar":aadhar,"aadhar_date":str(user.aadhar_date),"pan":pan,"pan_date":str(user.pan_date)}), 200

    def post(self):
        url = request.url
        if "login" in url:
            return self.login()
        elif "register" in url:
            return self.register()

    def get(self):
        url = request.url
        if "profile" in url:
            return self.profile()
