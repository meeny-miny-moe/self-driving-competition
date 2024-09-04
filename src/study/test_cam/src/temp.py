import cv2
import os

print("Current Working Directory:", os.getcwd())

img = cv2.imread('stop3.jpg')

cv2.imshow('test', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
