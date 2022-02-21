# Import essential libraries
import requests
import cv2
import numpy as np
import imutils
###########################
frameWidth = 1000
frameHeight = 680
minArea = 500
color = (255, 0, 255)
count = 0
#############################

plateCascade = cv2.CascadeClassifier('/home/dl7/nauka/Resources/haarcascade_russian_plate_number.xml')


# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = 'http://192.168.1.4:8080/shot.jpg'

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=frameWidth, height=frameHeight)



    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGrey, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(img, 'NumberPlate', (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,1 ,color, 2)
            imgRoi = img[y:y+h, x:x+w]
            cv2.imshow('Roi', imgRoi)
    cv2.imshow("Android_cam", img)

    # Press Esc key to exit
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('/home/dl7/nauka/Resources/Scanned/NoPlate_'+str(count)+'.jpg', imgRoi)
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 2)
        cv2.imshow('Result', img)
        cv2.waitKey(500)
        count += 1


cv2.destroyAllWindows()