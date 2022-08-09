import ml.OCR as OCR
import ml.AadharExtractor as AE

def getAadharDictionary(path):
    OCRList=OCR.getOCRList(path)
    Dict=AE.getAadharJSON(OCRList)
    return Dict

#use for testing the final code
# if __name__ == '__main__':
#     Dict= getAadharDictionary("/Users/aditya_gitte/Projects/SIH /Machine Learning/SampleFiles/Ath_aadharCard.jpeg")
#     print(Dict)