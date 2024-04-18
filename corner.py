import cv2 as cv
import numpy as np

# Reading an image 
img = cv.imread('test1.jpg')
cv.imshow("TicTacToe",img)

gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray",gray)
gray =np.float32(gray)
dst = cv.cornerHarris(src=gray,blockSize=2,ksize=3,k=0.04)
dst = cv.dilate(dst,None)
img[dst>0.01*dst.max()]=[255,0,0]
resized = cv.resize(img,(500,500),interpolation=cv.INTER_AREA)
cv.imshow("Corner detection",resized)

# PROBLEM: all unnecessary corners are also detected

cv.waitKey(0)