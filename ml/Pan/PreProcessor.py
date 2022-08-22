import cv2
import matplotlib.pyplot as plt






#path 1 is the path 1 of the original image and path 2 is the path of the pre-processed image
def panNumberSubImagePrePorcessor(path1,path2):
    img = cv2.imread(path1)
    plt.figure(figsize=(10, 6))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh8 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 22)

    bi_lat = cv2.bilateralFilter(thresh8, 9, 75, 75)
    denoised = cv2.fastNlMeansDenoising(bi_lat, 15, 10, 50)
    cv2.imwrite(path2, denoised)





