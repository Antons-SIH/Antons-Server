import json
from urllib import response
from sqlalchemy import null
from flask_restful import (Resource, reqparse, request)
from models.aicte import AicteModel
from models.uid import UidModel
from models.npci import NpciModel
from models.pan import PanModel
from util.response import HttpApiResponse, HttpErrorResponse
from util.jwt import createToken,decodeToken
from util.time import nowTime
import os,requests

class Verification(Resource):
    def AdminVerification(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            findUser=AicteModel.find_by_id(id)

            if(findUser.user_type=="Admin"):
                users=AicteModel.find_college_users(findUser.college)
                # print(users[0].user_type)
                #from UID database - phone,address
                #from NPCI databse - seeded_bank_acc
                
                for user in users:
                    if user.user_type=="Student" or user.user_type=="Teacher":
                        if(user.aadhar):
                            user_UID=UidModel.find_by_aadhar(user.aadhar)
                            user_NPCI=NpciModel.find_by_aadhar(user.aadhar)
                            postDict={'email':user.email,'msg':""}
                            if(user.phone!=user_UID.phone):
                                user.phone=user_UID.phone
                                user.last_updated=nowTime()
                                user.save_to_db()
                                postDict['msg']='Dear '+user.name+', your phone number has been updated on the AICTE portal as per the UID database. Please visit the AICTE portal for more details.'
                                requests.post(os.getenv("EMAIL_URL"),json=postDict)

                            if(user.address!=user_UID.address):
                                user.address=user_UID.address
                                user.last_updated=nowTime()
                                user.save_to_db()
                                postDict['msg']='Dear '+user.name+', your address has been updated on the AICTE portal as per the UID database. Please visit the AICTE portal for more details.'
                                requests.post(os.getenv("EMAIL_URL"),json=postDict)

                            if(user.seeded_bank_acc!=user_NPCI.seeded_bank_acc):
                                user.seeded_bank_acc=user_NPCI.seeded_bank_acc
                                user.last_updated=nowTime()
                                user.save_to_db()
                                postDict['msg']='Dear '+user.name+', your seeded-bank acount has been updated on the AICTE portal as per the NPCI database. Please visit the AICTE portal for more details.'
                                requests.post(os.getenv("EMAIL_URL"),json=postDict)

                return HttpApiResponse("Verification completed"),200
            else:
                return HttpErrorResponse("Details cannot be fetched. User not authorised!"),404
        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def SuperadminVerification(self):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            id=decodeToken(token)
            findUser=AicteModel.find_by_id(id)

            if(findUser.user_type=="Super"):
                users=AicteModel.find_all()

                for user in users:
                    if user.user_type=="Admin":
                        postDict={'email':user.email,'msg':"Please Send a verification mail to students of your respective college for updated status of data."}
                        requests.post(os.getenv("EMAIL_URL"),json=postDict)

                return HttpApiResponse("Verification mails sent!"),200

            else:
                return HttpErrorResponse("Details cannot be fetched. User not authorised!"),404
        else:
            return HttpErrorResponse("Access Denied!Access Token not found!"),404

    def get(self):
        url=request.url
        if "admin" in url:
            return self.AdminVerification()
        if "super" in url:
            return self.SuperadminVerification()
