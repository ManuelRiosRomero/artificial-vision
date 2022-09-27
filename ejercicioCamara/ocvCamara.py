# Call the required package
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import math

def tilt(img):
    rows,cols= img.shape[1], img.shape[0]
    pts1 = np.float32([[500,500],[200,5],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])
    M = cv2.getAffineTransform(pts1,pts2)
    return cv2.warpAffine(img,M,(cols,rows))

def  persp(img):
    rows1,cols2= img.shape[1], img.shape[0]
    pts1 = np.float32([[56,65],[368,2],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,500],[300,300]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    return cv2.warpPerspective(img,M,(300,300))

def calculate_func(img):
    return  tilt(img)

img = cv2.imread('b.jpg', cv2.IMREAD_UNCHANGED)
func = calculate_func(img)
perpe=persp(img)
cv2.imwrite('tilt.jpg', func)
cv2.imwrite('persp.jpg', perpe)