import ml.Aadhar.PreProcessor as PreProcessor
import ml.Aadhar.OCR as OCR
import ml.Aadhar.AadharExtractor as AE

def getAadharDictionary(path):
    PreProcessor.removeMarathiWordsfromImage(path)
    OCRList=OCR.getOCRList(path)
    Dict=AE.getAadharDict(OCRList)
    return Dict

#use for testing the final code
# if __name__ == '__main__':
#     Dict= getAadharDictionary("/Users/aditya_gitte/Projects/SIH/Machine_Learning/SampleFiles/Ath_aadharCard.jpeg")
#     print(Dict)