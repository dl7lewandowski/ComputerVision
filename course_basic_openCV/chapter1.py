import cv2
# load image from file

# img = cv2.imread('/home/dl7/nauka/females-g345b85309_640.jpg')
#
# cv2.imshow('output', img)
# cv2.waitKey(0)
#

# load video from file
# cap = cv2.VideoCapture('/home/dl7/nauka/Sand - 73847.mp4')
# while True:
#     success, img = cap.read()
#     cv2.imshow('Video', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# video camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)
while True:
    success, img = cap.read()
    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break