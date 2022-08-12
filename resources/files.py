from flask_restful import Resource, Api, reqparse, request
import werkzeug
from ml.OCR_dictionary import getAadharDictionary

class UploadAadhar(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name+'.aadhar')
        Dict= getAadharDictionary('images/'+name+'.aadhar')
        return ({"messag":"file received successfully!","filename":name, "data":Dict})


class UploadPan(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name+'.pan')
        return ({"messag":"Pan received successfully!", "filename":name})