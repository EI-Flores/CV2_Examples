import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.5)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"," "],
        ["Z","X","C","V","B","N","M",",","/","?"]]

textoFinal = ""


def drawAll(img, btnList):
    for btn in btnList:
        x, y = btn.pos
        w, h = btn.size
        cvzone.cornerRect(img, (btn.pos[0], btn.pos[1], btn.size[0], btn.size[1]),
                           20, rt=0)
        cv2.rectangle(img, btn.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED) 
        cv2.putText(img,btn.text,(x+10,y+50), cv2.FONT_HERSHEY_PLAIN,
                        4, (255, 255, 255), 4)
    return img

# def drawAll(img, btnList):
#     imgNuevo = np.zeros_like(img, uint8)
#     for btn in btnList:
#         x, y = btn.pos
#         cvzone.cornerRect(imgNuevo, (btn.pos[0], btn.pos[1], btn.size[0], btn.size[1]),
#                             20, rt=0)
#         cv2.rectangle(imgNuevo, btn.pos, (x + btn.size[0], y + btn.size[1]),
#                        (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNuevo, btn.text, (x + 40, y + 60),
#                      cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

#     out = img.copy()
#     alpha = 0.8
#     mask = imgNuevo.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNuevo, 1 - alpha, 0)[mask]
#     return out

class btn():
    def __init__(self, pos, text, size=[65,60]):
        self.pos = pos
        self.size = size
        self.text = text
    

btnList = []
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            btnList.append(btn([100*j+50,80*i+70], key))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, btnList)

    
    if lmList:
        for btn in btnList:
            x, y = btn.pos
            w, h = btn.size
            if (x < lmList[8][0] < x+w) and (y < lmList[8][1] < y+h):
                cv2.rectangle(img, (x-10, y-10), (x+w+8, y+h+8), (255, 0, 0), cv2.FILLED) 
                cv2.putText(img,btn.text,(x+10,y+50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw =False)
                #print(l)

                #When user "click"
                if l<30:
                    #cv2.rectangle(img, btn.pos, (x+w, y+h), (0, 255, 255), cv2.FILLED)
                    cv2.rectangle(img, btn.pos, (x+w, y+h), (0, 0, 255), 10) 
                    cv2.putText(img,btn.text,(x+10,y+50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
                    textoFinal += btn.text
                    sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (234, 255, 0), cv2.FILLED) 
    cv2.putText(img,textoFinal ,(60, 425), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv2.imshow("Imagen", img)
    if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()