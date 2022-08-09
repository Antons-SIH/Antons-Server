from unicodedata import name
import ml.OCR as OCR


def isEnglish(str):
    return str.isascii()


def matchesDateFormat(str):
    slashCounter = 0
    for i in str:
        if i == '/':
            slashCounter += 1
    if slashCounter == 2:
        return True
    else:
        return False


def matchesAadharFormat(str):
    if len(str) == 14 and str[4] == " " and str[9] == " ":
        return True


def getAadharJSON(OcrList):
    aadharNumber = ""
    dob = ""
    gender = ""  # F for female and M for Male
    name = ""

    aadharFlag = False
    dobFlag = False
    genderFlag = False
    nameFlag = False

    # dob detector
    eleCounter = 0
    for ele in OcrList:
        if matchesDateFormat(ele):
            dobFlag = True
            opstr = ""
            counter = 0
            for i in ele:
                if i == '/':
                    opstr = ele[counter - 2] + ele[counter - 1] + ele[counter] + ele[counter + 1] + ele[counter + 2] + \
                            ele[counter + 3] + ele[counter + 4] + ele[counter + 5] + ele[counter + 6] + ele[counter + 7]
                    dob = opstr
                    garbage = OcrList.pop(eleCounter)
                    break
                counter += 1
        eleCounter += 1

    # aadhar number detector
    eleCounter = 0
    for ele in OcrList:
        if matchesAadharFormat(ele):
            aadharFlag = True
            aadharNumber = ele
            aadharNumber = aadharNumber.replace(" ", "")
            garbage = OcrList.pop(eleCounter)
            break
        eleCounter += 1

    # gender detector
    eleCounter = 0
    for ele in OcrList:
        lowerCaseEle = ele.lower()
        if "female" in lowerCaseEle or "fmale" in lowerCaseEle:
            gender = "F"
            genderFlag = True
            garbage = OcrList.pop(eleCounter)
            break
        elif "male" in lowerCaseEle:
            gender = "M"
            genderFlag = True
            garbage = OcrList.pop(eleCounter)
            break
        eleCounter += 1

    # removing marathi text
    eleCounter = 0
    poppingList = []
    for ele in OcrList:
        if isEnglish(ele) == False:
            poppingList.append(eleCounter)
        eleCounter += 1
    poppingList.reverse()
    for i in poppingList:
        garbage = OcrList.pop(i)

    nameFlag = True
    name = OcrList.pop(1)

    Dict = {}
    if nameFlag == True:

        Dict["name"] = name
    else:
        Dict["name"] = "NA"

    if dobFlag == True:
        Dict["dob"] = dob
    else:
        Dict["dob"] = "NA"

    if aadharFlag == True:
        Dict["aadharNumber"] = aadharNumber
    else:
        Dict["aadharNumber"] = "NA"

    if genderFlag == True:
        Dict["gender"] = gender
    else:
        Dict["gender"] = "NA"

    return Dict

    # testing
    # print(Dict)
    # print(dob)
    # print(aadharNumber)
    # print(gender)
    # print(name)
    # print(OcrList)

# if __name__ == "__main__":
#     getAadharJSON(OCR.getOCRList("/Users/aditya_gitte/Projects/SIH /SampleFiles/aditya_aadhar.jpeg"))
