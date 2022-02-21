import cv2
import numpy as np

path = '/home/dl7/nauka/'
faceCascade = cv2.CascadeClassifier('/home/dl7/nauka/Resources/haarcascade_frontalface_default.xml')
img = cv2.imread(r'/home/dl7/nauka/face.jpg')


imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGrey, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)


cv2.imshow('Face', img)
cv2.waitKey(0)