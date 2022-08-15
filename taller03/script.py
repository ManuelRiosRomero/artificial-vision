# Call the required package
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import math


def translate(img):
    rows, cols = img.shape[1], img.shape[0]
    M = np.float32([[1, 0, 42], [0, 1, 37]])
    return cv2.warpAffine(img, M, (cols, rows))


def rotation(img):
    rows, cols = img.shape[1], img.shape[0]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 65, 1)
    return cv2.warpAffine(img, M, (cols, rows))


def scaled(img):
    scale_percent = 75
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dsize = (width, height)
    return cv2.resize(img, dsize)


def calculate_func(img):
    dst = scaled(img)
    dst = translate(dst)
    return rotation(dst)


def scaled_matrix(img):
    rows, cols = img.shape[1], img.shape[0]
    #aux1 = 0.75*math.cos(65)*42+(-0.75*math.sin(65)*-37)
    #aux2 = 0.75*math.sin(65)*42+(0.75*math.cos(65)*-37)
    M = np.float32([[0.31696, -0.67973, 38.4623],
                   [0.67973, 0.31696, 16.8211]])
    return cv2.warpAffine(img, M, (cols, rows))


def calculate_matrix(img):
    pass


img = cv2.imread('b.jpg', cv2.IMREAD_UNCHANGED)

func = calculate_func(img)
mat = scaled_matrix(img)
cv2.imwrite('functions.jpg', func)
cv2.imwrite('matrix.jpg', mat)
