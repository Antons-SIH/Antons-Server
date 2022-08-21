from flask_restful import Resource, Api, reqparse
from flask import request
import werkzeug, os
from models.aicte import AicteModel
from util.response import HttpApiResponse, HttpErrorResponse
import threading, requests, time

class UploadAadhar(Resource):
    def post(self):

        user_email = request.form['email']
        image_file = request.files['file']

        ## Check if user exist with this email
        user = AicteModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Get image and upload for analysis
        name=image_file.filename
        image_file.save('images/'+name)

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


class UploadPan(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name+'.pan')
        return ({"messag":"Pan received successfully!", "filename":name})