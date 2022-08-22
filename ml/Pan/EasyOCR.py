import easyocr
import PIL


def getOCRText(path):
    im = PIL.Image.open(path)

    reader = easyocr.Reader(['en'])
    # Bounds = reader.readtext(path, text_threshold=0.95, contrast_ths=0.35, adjust_contrast=0.05, add_margin=0.1, width_ths=0.7, decoder='beamsearch')
    Bounds = reader.readtext(path, text_threshold=0.95, contrast_ths=0.35, adjust_contrast=0.05, add_margin=0.1, width_ths=2, decoder='beamsearch')
    finalList = []

    # return Bounds[0][1]
    for item in Bounds:
        finalList.append(item[1])
    if len(finalList)==0:
        return "Nothing"
    else:
        str=finalList[0].strip()
        return str



# testing code
# path="/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/Pan/Dump/orig_img2.jpeg"
# str=list=getOCRText(path)
# print(str)