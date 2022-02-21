import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import pynput



cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height

detector = HandDetector(detectionCon=0.8, maxHands=1)

keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

finalText = ''

def drawAll(img, buttonList):

    for button in buttonList:

        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w,y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1]+ 65), cv2.FONT_HERSHEY_PLAIN, 4, ((255, 255, 255)), 4)

    return img
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text



buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))



while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=True)
    img = drawAll(img, buttonList)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1['lmList']

        if lmList1:

            for button in buttonList:
                x, y = button.pos
                w, h = button.size


                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                ((255, 255, 255)), 4)
                    l, _, _ = detector.findDistance(lmList1[8], lmList1[4], img)
                    print(l)

                    # When clicked
                    if l < 30:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 65), cv2.FONT_HERSHEY_PLAIN,
                                    4,
                                    ((255, 255, 255)), 4)
                        finalText += button.text
                        sleep(0.1)
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60,  425), cv2.FONT_HERSHEY_PLAIN,
                5,
                ((255, 255, 255)), 5)

    cv2.imshow('Image', img)
    cv2.waitKey(1)