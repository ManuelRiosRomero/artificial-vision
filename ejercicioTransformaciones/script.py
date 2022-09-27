# Call the required package
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import math

def translate(img):
    rows, cols = img.shape[1], img.shape[0]
    M = np.float32([[1, 0, 42], [0, 1, -37]])
    return cv2.warpAffine(img, M, (cols, rows))

def rotation(img):
    rows, cols = img.shape[1], img.shape[0]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 65, 1)
    return cv2.warpAffine(img, M, (cols, rows))

def scaled(img):
    width = int(img.shape[1] * 0.75)
    height = int(img.shape[0] * 0.75)
    dsize = (width, height)
    return cv2.resize(img, dsize)

def calculate_func(img):
    dst = scaled(img)
    dst= rotation(dst)
    return  translate(dst)

def scaled_matrix(img):
    rows, cols = img.shape[1], img.shape[0]
    x,y=rows/2,cols/2
    M = np.float32([[0.31696, 0.67973, ((0.6835*x)-(0.6795*y)-11.8485)],
                  [-0.67973, 0.31696, ((0.6795*x)+(0.6835*y)-40.2495)]])
    return cv2.warpAffine(img, M, (rows, cols))

def calculate_matrix(img):
    pass

img = cv2.imread('b.jpg', cv2.IMREAD_UNCHANGED)

func = calculate_func(img)
mat = scaled_matrix(img)
cv2.imwrite('functions.jpg', func)
cv2.imwrite('matrix.jpg', mat)
