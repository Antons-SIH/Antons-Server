import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.aicte import AicteModel
from werkzeug.security import generate_password_hash, check_password_hash
from util.response import HttpApiResponse, HttpErrorResponse
from util.jwt import createToken,decodeToken
import random, math, requests,os
from twilio.rest import Client

class PhoneOtp(Resource):
    phone_parser = reqparse.RequestParser()
    phone_parser.add_argument('aadhar_phone', type=str, required=True, help="This field cannot be blank.")

    verify_parser = reqparse.RequestParser()
    verify_parser.add_argument('otp', type=str, required=True, help="This field cannot be blank.")

    def sendOtp(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            user=AicteModel.find_by_id(id)
            data = PhoneOtp.phone_parser.parse_args()
            if not user:
                return HttpErrorResponse({"message": "User does not exist"}), 401
            
            phone=data['aadhar_phone']
            phone='+91'+str(phone)
            digits = [i for i in range(0, 10)]
            otp = ""

            for i in range(6):
                index = math.floor(random.random() * 10)
                otp += str(digits[index])

            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                     body="OTP for authentication of uploading the document is : "+otp,
                     from_='+12136685431',
                     to=phone
                 )
            user.otp = otp
            user.save_to_db()
            print(message.sid)

            return HttpApiResponse({"message": "OTP sent successfully!"}), 201
        
        else:
            return HttpErrorResponse("Token Not found! Secured route access denied!"),404

    def verifyOtp(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            user=AicteModel.find_by_id(id)
            data = PhoneOtp.verify_parser.parse_args()
            if user.otp == data['otp']:
                return HttpApiResponse("Success"),200
            else:
                return HttpErrorResponse("Enter Correct OTP"),404
        else:
            return HttpErrorResponse("Access Denied! Access Token not found!"),404

    def post(self):
        url = request.url
        if "sendotp" in url:
            return self.sendOtp()
        elif "verifyotp" in url:
            return self.verifyOtp()

