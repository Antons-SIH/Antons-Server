import base64
from flask_restful import Resource, Api, reqparse
from flask import request
import werkzeug, os
from models.aicte import AicteModel
from util.response import HttpApiResponse, HttpErrorResponse
import threading, requests, time
from models.pan import PanModel 
# Check for user in AICTE database - DONE
# Upload Images, check if already present then do not go further
# Save image and make a new thread to take out the extracted text
# Check for the NA values
# Check for existing no. to be present in UID & NPCI database and update the fields
# If any changes in the fields then update last_updated
import base64

## This will just run first time to check the aadhar and get the user aadhar number
class UploadAadhar(Resource):
    def post(self):
        user_email = request.form['email']
        # image_file = request.files['file']
        filestring = request.form['filestring']

        decoded_data=base64.b64decode((filestring))
        img_file = open('aadhar.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
        name="aadhar"
        # print(image_file)
        ## Check if user exist with this email
        user = AicteModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Check if aadhar already present then don't go further
        if user.aadhar:
            return HttpErrorResponse ("Cannot upload, not a new user"), 400

        ## Get image and upload for analysis
        # name=image_file.filename
        # image_file.save('images/'+name)

        ## Add a thread to run the ML Aadhar Model in background 
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


## This will just run first time to check the aadhar and get the user pan number
class UploadPan(Resource):
    def post(self):

        user_email = request.form['email']
        image_file = request.files['file']

        ## Check if user exist with this email
        user = AicteModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Check if pan already present then don't go further
        if user.pan:
            return HttpErrorResponse ("Cannot upload, not a new user"), 400

        name='pan'
        image_file.save('images/'+name)

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