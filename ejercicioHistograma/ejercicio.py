from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np


def get_otsu_treshhold(image, th):
    # generar nueva prop img
    thresholded_im = np.zeros(image.shape)
    thresholded_im[image >= th] = 1

    # generar pesos
    nb_pixels = image.size
    nb_pixels1 = np.count_nonzero(thresholded_im)
    weight1 = nb_pixels1 / nb_pixels
    weight0 = 1 - weight1

    if weight1 == 0 or weight0 == 0:
        return np.inf

    # encontrar pixeles de clase
    val_pixels1 = image[thresholded_im == 1]
    val_pixels0 = image[thresholded_im == 0]

    var0 = np.var(val_pixels0) if len(val_pixels0) > 0 else 0
    var1 = np.var(val_pixels1) if len(val_pixels1) > 0 else 0

    return weight0 * var0 + weight1 * var1

image = cv.imread("b.jpg")

threshold_range = range(np.max(image)+1)
criterias = [get_otsu_treshhold(image, th) for th in threshold_range]


otsu_threshold = threshold_range[np.argmin(criterias)]
print("------------------------------")
print("Umbral Calculado: ")
print(otsu_threshold)

ret,thresh1 = cv.threshold(image,otsu_threshold,255,cv.THRESH_BINARY)
ret,thresh4 = cv.threshold(image,otsu_threshold,255,cv.THRESH_TOZERO)

cv.imwrite("imagenBinarial.jpg",thresh1 )
cv.imwrite("imagenTruncado.jpg",thresh4 )
