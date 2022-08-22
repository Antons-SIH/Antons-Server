import pytesseract
import cv2
import matplotlib.pyplot as plt

#pass the path of the preprocessed imaage
def tessOCR(path):
    img=cv2.imread(path)
    custom_config ='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/ --psm 3 --oem 3'
    # custom_config ='--psm 3 --oem 3'

    text = pytesseract.image_to_string(img, config=custom_config, lang='eng')
    text=text.strip()

    return text
