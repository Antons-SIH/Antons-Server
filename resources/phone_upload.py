from flask_restful import Resource, Api, reqparse
from flask import request
import werkzeug, os
from models.aicte import AicteModel
from util.response import HttpApiResponse, HttpErrorResponse
import threading, requests, time
from models.pan import PanModel
import base64 

class AadharPhone(Resource):
    def post(self):
        user_email = request.form['email']
        filestring = request.form['filestring']

        user = AicteModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Check if aadhar already present then don't go further
        if user.aadhar:
            return HttpErrorResponse ("Cannot upload, not a new user"), 400

        filestring=filestring[23:]
            # filestring=filestring.rstrip(filestring[-1])
        decoded_data=base64.b64decode((filestring))
        img_file = open('images/image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
        name="aadhar.jpeg"

        def background_aadhar_model(**kwargs):
            time.sleep(3)
            user_email = kwargs.get('user_email', {})
            name = kwargs.get('name', {})
            postDict = {'user_email': user_email, 'name': name}
            requests.post(os.getenv("PROCESS_URL") + "/aadhar", json=postDict)

        ## Declare the thread target and send required arguments, then initiate it with thread.start()
        thread = threading.Thread(target=background_aadhar_model, kwargs={'user_email': user_email, 'name': name})
        thread.start()

        return HttpApiResponse("Successfully uploaded picture")

class PanPhone(Resource):
    def post(self):
        user_email = request.form['email']
        filestring = request.form['filestring']

        ## Check if user exist with this email
        user = AicteModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Check if pan already present then don't go further
        if user.pan:
            return HttpErrorResponse ("Cannot upload, not a new user"), 400

        filestring=filestring[23:]
            # filestring=filestring.rstrip(filestring[-1])
        decoded_data=base64.b64decode((filestring))
        img_file = open('images/image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
        name="pan.jpeg"

        ## Add a thread to run the ML Pan Model in background 
        def background_pan_model(**kwargs):
            time.sleep(3)
            user_email = kwargs.get('user_email', {})
            name = kwargs.get('name', {})
            postDict = {'user_email': user_email, 'name': name}
            requests.post(os.getenv("PROCESS_URL") + "/pan", json=postDict)

        ## Declare the thread target and send required arguments, then initiate it with thread.start()
        thread = threading.Thread(target=background_pan_model, kwargs={'user_email': user_email, 'name': name})
        thread.start()

        return HttpApiResponse("Successfully uploaded picture")

