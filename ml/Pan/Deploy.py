### importing required libraries
import torch
import cv2
import numpy as np
import PreProcessor as pp
import TesseractOCR as tess
import EasyOCR as es
import os

modelPath = "/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/Pan/yolov5"
weightsPath = "/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/Pan/best.pt"
dumpPath= "/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/Pan/Dump"

panNumber=""
panName=""
dob=""

def clearDump(dumpPath):
    dir = dumpPath
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))



### -------------------------------------- function to run detection ---------------------------------------------------------
def detectx(frame, model):
    frame = [frame]
    results = model(frame)
    labels, cordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    return labels, cordinates



### ------------------------------------ to plot the BBox and results --------------------------------------------------------
def plot_boxes(results, frame, classes):
    """
    --> This function takes results, frame and classes
    --> results: contains labels and coordinates predicted by model on the given frame
    --> classes: contains the starting labels
    """
    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    print(f"[INFO] Total {n} detections. . . ")
    print(f"[INFO] Looping through all detections. . . ")

    ### looping through the detections
    for i in range(n):

        row = cord[i]
        if row[4] >= 0.1:  ### threshold value for detection. We are discarding everything below this value
            print(f"[INFO] Extracting BBox coordinates. . .{labels[i]} ")
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                row[3] * y_shape)  ## BBOx coordniates
            text_d = classes[int(labels[i])]
            # cv2.imwrite("./output/dp.jpg",frame[int(y1):int(y2), int(x1):int(x2)])

            coords = [x1, y1, x2, y2]

            panOCR(img=frame, coords=coords, label=int(labels[i]))

    return frame


#### ---------------------------- function to recognize license plate --------------------------------------


# function to recognize license plate numbers using Tesseract OCR
def panOCR(img, coords, label):

    #testing code
    # print(f"received label {label}")

    # separate coordinates from box
    xmin, ymin, xmax, ymax = coords
    # get the subimage that makes up the bounded region and take an additional 2 pixels in the x direction
    nplate = img[int(ymin):int(ymax), int(xmin) - 2:int(xmax) + 2]
    global panNumber
    global panName
    global dob
    cv2.imwrite(f"{dumpPath}/orig_img{label}.jpeg", nplate)
    if label == 0:
        pp.panNumberSubImagePrePorcessor(
            f"{dumpPath}/orig_img0.jpeg",
            f"{dumpPath}/img0.jpg")
        panNumber= tess.tessOCR(f"{dumpPath}/img0.jpg")
        # print(panNumber)
    elif label==1:
        panName=es.getOCRText(f"{dumpPath}/orig_img1.jpeg")
        # print(panName)
    elif label==2:
        dob=es.getOCRText(f"{dumpPath}/orig_img2.jpeg")
        # print(dob)










### ---------------------------------------------- Main function -----------------------------------------------------

def main(img_path=None):
    print(f"[INFO] Loading model... ")
    ## loading the custom trained model

    model = torch.hub.load(modelPath, 'custom', source='local', path=weightsPath,
                           force_reload=True)  ### The repo is stored locally

    classes = model.names  ### class names in string format
    print(classes)

    ### --------------- for detection on image --------------------

    print(f"[INFO] Working with image: {img_path}")
    img_out_name = f"./output/result_{img_path.split('/')[-1]}"

    frame = cv2.imread(img_path)  ### reading the image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = detectx(frame, model=model)  ### DETECTION HAPPENING HERE

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    frame = plot_boxes(results, frame, classes=classes)


# clearDump(dumpPath)
main(img_path="/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/SampleImages/Pan/6.jpeg")
# print(panName)
# print(panNumber)
# print(dob)
Dict = {1: panNumber, 2: panName, 3: dob}
print(Dict)
def getPanDict(path):
    clearDump(dumpPath)
    main(img_path="/Users/aditya_gitte/Projects/SIH/Antons-ML-Model/SampleImages/Pan/6.jpeg")
    global Dict
    Dict = {1: panNumber, 2: panName, 3: dob}
