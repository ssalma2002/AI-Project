import cv2 as cv
import numpy as np

# Reading an image 
img = cv.imread('test1.jpg')
cv.imshow("TicTacToe",img)

# Creating a blank image
blank= np.zeros(img.shape,dtype="uint8")
# cv.imshow("Blank",blank)

gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray",gray)

blur= cv.GaussianBlur(gray,(5,5),cv.BORDER_DEFAULT)
# cv.imshow("Blur",blur)

canny2 = cv.Canny(blur,125,175)
# cv.imshow("Canny 2",canny2)

# ret,thresh= cv.threshold(gray,125,255,cv.THRESH_BINARY)
# cv.imshow("Thresh",thresh)

# Get contours
contours,hierarchies = cv.findContours(canny2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
# print(f"Number of countours {len(contours)}")

# Draw Contour on the blank image that has been created
contour =cv.drawContours(blank,contours,-1,(255,255,255),2)
# cv.imshow("Draw Contour on blank",blank)

# Resizing the image
resized = cv.resize(contour,(500,500),interpolation=cv.INTER_AREA)
cv.imshow('Resized',resized)





cv.waitKey(0)