# 0:pan number 1:pan name 2:dob
import torch
import cv2
import numpy as np
import PreProcessor as pp
import TesseractOCR as tess
import EasyOCR as es
import os


class PanDictionary:
    model=None
    classes=None
    modelPath=None
    weightsPath=None
    dumpPath=None
    imgPath=None
    panNumber = "NA"
    panName = "NA"
    dob = "NA"



    def __init__(self,modelPath,weightsPath,dumpPath,imgPath):
        self.modelPath=modelPath
        self.weightsPath=weightsPath
        self.dumpPath=dumpPath
        self.model=torch.hub.load(self.modelPath, 'custom', source='local', path=self.weightsPath,
                           force_reload=True)
        self.classes=self.model.names
        self.imgPath=imgPath

    def clearDump(self):
        dir = self.dumpPath
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))


    def detectx(self,frame):
        frame = [frame]
        results = self.model(frame)
        labels, cordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cordinates

    def panOCR(self,img, coords, label):

        # testing code
        # print(f"received label {label}")

        # separate coordinates from box
        xmin, ymin, xmax, ymax = coords
        # get the subimage that makes up the bounded region and take an additional 2 pixels in the x direction
        nplate = img[int(ymin) - 1:int(ymax) + 1, int(xmin) - 2:int(xmax) + 2]
        global panNumber
        global panName
        global dob
        cv2.imwrite(f"{self.dumpPath}/orig_img{label}.jpeg", nplate)
        if label == 0:
            pp.panNumberSubImagePrePorcessor(
                f"{self.dumpPath}/orig_img0.jpeg",
                f"{self.dumpPath}/img0.jpg")
            self.panNumber = tess.tessOCR(f"{self.dumpPath}/img0.jpg")
            # print(panNumber)
        elif label == 1:
            self.panName = es.getOCRText(f"{self.dumpPath}/orig_img1.jpeg")
            # print(panName)
        elif label == 2:
            self.dob = es.getOCRText(f"{self.dumpPath}/orig_img2.jpeg")
            # print(dob)


    def plot_boxes(self,results, frame):

        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]

        # print(f"[INFO] Total {n} detections. . . ")
        # print(f"[INFO] Looping through all detections. . . ")

        ### looping through the detections
        for i in range(n):

            row = cord[i]
            if row[4] >= 0.1:  ### threshold value for detection. We are discarding everything below this value
                # print(f"[INFO] Extracting BBox coordinates. . .{labels[i]} ")
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)  ## BBOx coordniates
                text_d = self.classes[int(labels[i])]
                # cv2.imwrite("./output/dp.jpg",frame[int(y1):int(y2), int(x1):int(x2)])

                coords = [x1, y1, x2, y2]

                self.panOCR(img=frame, coords=coords, label=int(labels[i]))

        return frame



    def generatePandict(self):
        frame = cv2.imread(self.imgPath)  ### reading the image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.detectx(frame)  ### DETECTION HAPPENING HERE

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        frame = self.plot_boxes(results, frame)

    def getPanNumber(self):
        self.clearDump()
        self.generatePandict()
        # Dict = {0: self.panNumber, 1: self.panName, 2: self.dob}
        self.clearDump()
        return self.panNumber


if __name__ == '__main__':

    f = open("write.txt", "w")
    f.write("NA")
    f.close()

    obj=PanDictionary("ml/Pan/yolov5","ml/Pan/best.pt","ml/Pan/Dump","images/pan")
    str=obj.getPanNumber()
    print(str)
    if not str:
        str="NA"
    f = open("write.txt", "w")
    f.write(str)
    f.close()
