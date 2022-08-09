import easyocr
import PIL


def getOCRList(path):
    im = PIL.Image.open(path)
    print(type(im))
    reader = easyocr.Reader(['en', 'mr'])
    # Bounds = reader.readtext(path, text_threshold=0.95, contrast_ths=0.35, adjust_contrast=0.05, add_margin=0.1, width_ths=0.7, decoder='beamsearch')
    Bounds = reader.readtext(path, text_threshold=0.95, contrast_ths=0.35, adjust_contrast=0.05, add_margin=0.1, width_ths=2, decoder='beamsearch')
    finalList = []
    for item in Bounds:
        finalList.append(item[1])
    return finalList


# testing code
# path="/Users/aditya_gitte/Projects/SIH /SampleFiles/aditya_aadhar.jpeg"
# list=getOCRList(path)
# for i in list:
#     print(i)
