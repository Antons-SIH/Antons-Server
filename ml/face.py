import cv2
import face_recognition

# path1=r"C:\Users\dell\Desktop\face detector\Test\Atharva Nagmoti.jpg"
# path2=r"C:\Users\dell\Desktop\face detector\Images\23253_Atharva.jpeg"
def Facerec(path1,path2):
    

#Encode faces from a folder
# sfr = SimpleFacerec()
# sfr.load_encoding_images("Test/")
    print(path1, path2)
    img = cv2.imread(path1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    # print(face_recognition.face_encodings(rgb_img))
    print(len(face_recognition.face_encodings(rgb_img)))
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    img2 = cv2.imread(path2)
    # half = cv2.resize(img2, (0,0), fx = 0.5, fy = 0.5) 
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) 
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

    result = face_recognition.compare_faces([img_encoding], img_encoding2)
    print("face check done")
    return result[0]

# if __name__=='__main__':
#     path1=r"C:\Users\dell\Desktop\face detector\Test\Atharva Nagmoti.jpg"
#     path2=r"C:\Users\dell\Desktop\face detector\Images\23253_Atharva.jpeg"