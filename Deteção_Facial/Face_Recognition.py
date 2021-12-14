import cv2 as cv
import numpy as np
import face_recognition as fr
import os 





path = 'Faces'
images = []
names = []
mylist = os.listdir(path)

def findEncondings(image_List):
    encodeList = []
    for img in image_List:
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

for pathimg in mylist:
    current_img = cv.imread(f'{path}/{pathimg}')
    images.append(current_img)
    names.append(os.path.splitext(pathimg)[0])




EncodeList = findEncondings(images)

print('Encoding Complete')

cap = cv.VideoCapture(0)

while True:
    success, img = cap.read()
    
    imgS = cv.resize(img,(0,0),None,0.25,0.25)
    imgS = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    
    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS,facesCurFrame)

    for encondeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = fr.compare_faces(EncodeList, encondeFace)
        faceDist = fr.face_distance(EncodeList, encondeFace)
        matchIndex = np.argmin(faceDist)
        print(np.amin(faceDist))
        
        if np.amin(faceDist) < 0.4:
            if matches[matchIndex]:
                name = names[matchIndex].upper()
                print( name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
        
        else:
            print("Desconhecido. Acesso negado!")
            
            
    # img = cv.flip(img,1)
    cv.imshow('webcam',img)
    cv.waitKey(1)           	
		


