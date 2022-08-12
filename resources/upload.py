from flask_restful import Resource, Api, reqparse, request
import werkzeug
from ml.OCR_dictionary import getAadharDictionary
from models.aicte import AicteModel
from models.uid import UidModel
from util.response import HttpApiResponse, HttpErrorResponse

class UploadAadhar(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        ## Get image and save it to a local location for analysis
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name+'.aadhar')

        ## Send it to the ML model to extract the card details
        Dict = getAadharDictionary('images/'+name+'.aadhar')
        print ({"message":"file received successfully!","filename":name, "data":Dict})
        aadharNumber = Dict["aadharNumber"]

        ## If aadhar NA then upload again
        if aadharNumber == 'NA':
            return HttpErrorResponse ("Upload again, image not clear"), 400

        ## Check it with AICTE database
        aicteData = AicteModel.find_by_aadhar(aadharNumber)
        if not aicteData:
            return HttpErrorResponse ("aadhar not found in aicte database, exiting the process"), 404

        print({"message":"Verified from AICTE Database", "aadharNumber":aadharNumber, "aicteData": aicteData})

        ## Check it with UID database
        uidData = UidModel.find_by_aadhar(aadharNumber)
        if not uidData:
            print({"message":"Aadhar does not exists in UID database","aadharNumber":aadharNumber})
            uidVerified = False
        else:
            print({"message":"Aadhar Verified from UID Database","aadharNumber":aadharNumber})
            uidVerified = True

        ## Check it with NPCI database
        npciData = UidModel.find_by_aadhar(aadharNumber)
        if not npciData:
            print({"message":"Aadhar does not exists in NPCI database","aadharNumber":aadharNumber})
            npciVerified = False
        else:
            print({"message":"Aadhar Verified from NPCI Database and recieved bank number","aadharNumber":aadharNumber})
            npciVerified = True

        ## Send the final result if UID and NPCI is verified or not
        return HttpApiResponse({'aadharVerified': uidVerified, 'npciVerified': npciVerified}), 200


class UploadPan(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        name=image_file.filename
        image_file.save('images/'+name+'.pan')
        return ({"messag":"Pan received successfully!", "filename":name})