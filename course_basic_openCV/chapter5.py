import cv2
import numpy as np

img = cv2.imread('/home/dl7/nauka/cards.png')

width, height = 250, 350
pts1 = np.float32([[299,161], [344,166], [301, 229], [342,229]])
pts2 = np.float32([[0,0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))
cv2.imshow('Output', imgOutput)

cv2.imshow('lambo', img)

cv2.waitKey(0)