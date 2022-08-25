import ml.Aadhar.OCR


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
    flag = True
    str = str.replace(" ", "")
    counter=0
    for char in str:
        if char.isdigit():
            counter+=1
    
    if counter == 12:
        flag=True

    else:
        flag = False
    return flag


def getAadharDict(OcrList):
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
            ano=""
            for char in ele:
                if char.isdigit()==True:
                    ano+=char
            aadharFlag = True
            aadharNumber = ano
            
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

    # removing marathi text in case some of it makes it through the pre-processor
    eleCounter = 0
    poppingList = []
    for ele in OcrList:
        if isEnglish(ele) == False:
            poppingList.append(eleCounter)
        eleCounter += 1
    poppingList.reverse()
    for i in poppingList:
        garbage = OcrList.pop(i)

    if(len(OcrList)>=2):
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
    #
    # print(dob)
    # print(aadharNumber)
    # print(gender)
    # print(name)
    # print(OcrList)

# if __name__ == "__main__":
#     print (OCR.getOCRList("/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/SampleImages/Aadhar/Aditya.png"))
