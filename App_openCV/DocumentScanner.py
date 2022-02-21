import numpy as np
import cv2
import requests
import time


frameWidth = 640
frameHeight = 480

widthImg = 640
heightImg = 480

cap = cv2.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10, 150)

def preProccesing(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)

    return imgThres

def getContoures(img):

    maxArea = 0
    biggest = np.array([])
    contoures, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contoures:
        area = cv2.contourArea(cnt)
        if area > 3000:
            # cv2.drawContours(imgContur, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContur, biggest, -1, (255, 0, 0), 30)

    return biggest

def reorder(myPoints):

    myPoints = myPoints.reshape((4,2))
    myNewPoints = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myNewPoints[0] = np.argmin(add)
    myNewPoints[3] = np.argmax(add)
    diff = np.diff(myPoints, 1)
    myNewPoints[1] = np.argmin(diff)
    myNewPoints[2] = np.argmax(diff)

    return myNewPoints

def getWrap(img, biggest):

    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0], [widthImg, 0], [0, heightImg], [widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    return imgOutput



url = 'http://192.168.1.4:8080/shot.jpg'

while True:

    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (widthImg, heightImg))

    imgContur = img.copy()

    imgThres = preProccesing(img)

    biggest = getContoures(imgContur)

    # imgWrap = getWrap(img, biggest)
    cv2.imshow("Camera", biggest)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


