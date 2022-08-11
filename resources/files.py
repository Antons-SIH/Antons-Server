from flask_restful import Resource, Api, reqparse, request
import werkzeug
from ml.OCR_dictionary import getAadharDictionary

class UploadImage(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name)
        Dict= getAadharDictionary('images/'+name)
        return ({"messag":"file received successfully!","filename":name, "data":Dict})