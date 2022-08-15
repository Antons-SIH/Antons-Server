from flask_restful import Resource, Api, reqparse
from flask import request
import werkzeug
from models.user import UserModel
from util.response import HttpApiResponse, HttpErrorResponse
import threading
import requests

class UploadAadhar(Resource):
    def post(self):

        user_email = request.form['email']
        image_file = request.files['file']

        ## Check if user exist with this email
        user = UserModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404

        ## Get image and save it to a local location for analysis
        name=image_file.filename
        image_file.save('images/'+name)

        def long_running_task(**kwargs):
            user_email = kwargs.get('user_email', {})
            name = kwargs.get('name', {})
            postDict = {'user_email': user_email, 'name': name}
            requests.post('http://localhost:5000/api/image/process/aadhar', json=postDict)

        thread = threading.Thread(target=long_running_task, kwargs={'user_email': user_email, 'name': name})
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