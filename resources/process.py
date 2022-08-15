from flask_restful import Resource, Api, reqparse
from flask import request
from ml.OCR_dictionary import getAadharDictionary
from models.aicte import AicteModel
from models.uid import UidModel
from models.npci import NpciModel
from models.user import UserModel
from util.response import HttpApiResponse, HttpErrorResponse
from util.time import nowTime

class ProcessAadhar(Resource):
    def post(self):

        ## Get the data from [Upload:UploadAadhar] 
        input_json = request.get_json(force=True) 
        user_email = input_json['user_email']
        name = input_json['name']

        ## Get user and set remarks of aadhar and seeded bank to verifying for frontend
        user = UserModel.find_by_email(user_email)
        if not user:
            return HttpErrorResponse ("No user found with this email"), 404
        user.aadhar_remark = 'Verifying Uploaded Data'
        user.seeded_remark = 'Verifying Uploaded Data'
        user.save_to_db()

        ## Send it to the ML model to extract the card details
        Dict = getAadharDictionary('images/'+name)
        aadharNumber = Dict["aadharNumber"]
        print('[Process:ProcessAadhar] Aadhar model execution done | User='+ user_email + ' | AadharNo='+ aadharNumber)

        ## If aadhar NA then upload again
        if aadharNumber == 'NA':
            print('[Process:ProcessAadhar] Upload again, aadhar image not clear | User='+ user_email + ' | --ExitProcess--')
            user.aadhar_remark = 'Upload aadhar again, image not clear'
            user.seeded_remark = 'Upload aadhar again, image not clear'
            user.save_to_db()
            return HttpErrorResponse ("Upload again, image not clear"), 400

        ## Check it with AICTE database
        aicteData = AicteModel.find_by_aadhar(aadharNumber)
        if not aicteData:
            print('[Process:ProcessAadhar] Aadhar does not exists in AICTE database | AadharNo='+ aadharNumber + ' | --ExitProcess--')
            user.aadhar_remark = 'Failed, Aadhar does not exist with AICTE'
            user.seeded_remark = 'Failed, Aadhar does not exist with AICTE'
            user.save_to_db()
            return HttpErrorResponse ('Aadhar does not exists in AICTE database'), 404

        print('[Process:ProcessAadhar] Verified aadhar from AICTE Database | AadharNo='+ aadharNumber)

        ## Check it with UID database
        uidData = UidModel.find_by_aadhar(aadharNumber)
        if not uidData:
            print('[Process:ProcessAadhar] Aadhar does not exists in UID database | AadharNo='+ aadharNumber)
            user.aadhar_remark = 'Failed, Aadhar does not exist with UID'
            user.save_to_db()
            uidVerified = False
        else:
            user.aadhar = aadharNumber
            user.aadhar_remark = 'Aadhar Verified Successfully'
            user.aadhar_date = nowTime()
            user.updated_at = nowTime()
            user.save_to_db()
            print('[Process:ProcessAadhar] Verified aadhar from UID Database | AadharNo='+ aadharNumber)
            uidVerified = True

        ## Check it with NPCI database
        npciData = NpciModel.find_by_aadhar(aadharNumber)
        if not npciData:
            print('[Process:ProcessAadhar] Aadhar does not exists in NPCI database | AadharNo='+ aadharNumber)
            user.seeded_remark = 'Failed, Aadhar does not exist with NPCI'
            user.save_to_db()
            npciVerified = False
        else:
            user.seeded_bank_acc = npciData.seeded_bank_acc
            user.seeded_remark = 'Seeded Bank Verified Successfully'
            user.seeded_date = nowTime()
            user.updated_at = nowTime()
            user.save_to_db()
            print('[Process:ProcessAadhar] Verified aadhar from NPCI Database | AadharNo='+ aadharNumber)
            npciVerified = True

        ## Send the final result if UID and NPCI is verified or not
        return HttpApiResponse({'aadharVerified': uidVerified, 'npciVerified': npciVerified}), 200
