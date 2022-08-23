"""
1. Para un tipo de filtro particular, ¿aplicarlo 5 veces consecutivas sobre la imagen
utilizando un tamaño de ventana o kernel de 3x3 genera el mismo resultado que
aplicarlo una única vez con un tamaño de ventana o kernel de 11x11? ¿Para qué tipos de
filtros es esto válido? ¿Entre la dos versiones, cual sería la más rápida de aplicar?
"""

import cv2 as cv
import numpy as np
import time

imageName = 'img.jpg'
# Loads an image
src = cv.imread(cv.samples.findFile(imageName), cv.IMREAD_COLOR)

# Initialize ddepth argument for the filter
ddepth = -1
## --------Kernel Size setter---------------
def kernel_setter(kernel_size):
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
    kernel /= (kernel_size * kernel_size)
    return kernel

## ------------------Gaussian Blur--------------------
def gauss_func(img, kernel):
    for i in range(1, kernel, 2):
        dst = cv.GaussianBlur(img, (i, i), 0)
    return dst

## ---------Kernel size 3 called 5 times
def gauss_blurs_3():
    start = time.time()
    dst = gauss_func(src, 3) #1
    dst = gauss_func(dst, 3) #2
    dst = gauss_func(dst, 3) #3
    dst = gauss_func(dst, 3) #4
    dst = gauss_func(dst, 3) #5
    end = time.time()
    print("Time 3x3 kernel, gauss blur: ")
    print(end - start)
    cv.imwrite('gaussblur_kernel3r.jpg', dst)

## ---------Kernel size 11 call
def gauss_blurs_11():
    start = time.time()
    dst = gauss_func(src, 11) #
    end = time.time()
    print("Time 11x11 kernel, gauss blur: ")
    print(end - start)
    cv.imwrite('gaussblur_kernel11.jpg', dst)

## ----------------------filter2D----------------------
# ----Kernel size 3 called 5 times
def filter2d_blurs_3():
    kernel = kernel_setter(3)
    start = time.time()
    dst = cv.filter2D(src, ddepth, kernel) #1
    dst = cv.filter2D(dst, ddepth, kernel) #2
    dst = cv.filter2D(dst, ddepth, kernel) #3
    dst = cv.filter2D(dst, ddepth, kernel) #4
    dst = cv.filter2D(dst, ddepth, kernel) #5
    end = time.time()
    print("Time 3x3 kernel, filter2D: ")
    print(end - start)
    cv.imwrite('filter2d_kernel3.jpg', dst)

# ----Kernel size 11
def filter2d_blurs_11():
    kernel = kernel_setter(11)
    start = time.time()
    dst = cv.filter2D(src, ddepth, kernel)
    end = time.time()
    print("Time 11x11 kernel, filter2D: ")
    print(end - start)
    cv.imwrite('filter2d_kernel11.jpg', dst)

##--------------Median Blur--------------------------
#-----def function----

def median_func(img, kernel):    
    for i in range(1, kernel, 2):
        dst = cv.medianBlur(img, i)
    return dst

# ----Kernel size 3 called 5 times
def median_blurs_3():
    start = time.time()
    dst = median_func(src, 3) #1
    dst = median_func(dst, 3) #2
    dst = median_func(dst, 3) #3
    dst = median_func(dst, 3) #4
    dst = median_func(dst, 3) #5
    end = time.time()
    print("Time 3x3 kernel, median blur: ")
    print(end - start)
    cv.imwrite('medianblur_kernel3.jpg', dst)
#----Kernel size 11
def median_blurs_11():
    start = time.time()
    dst = median_func(src, 11) #1
    end = time.time()
    print("Time 11x11 kernel, median blur: ")
    print(end - start)
    cv.imwrite('medianblur_kernel11.jpg', dst)


## --------------------------------------------
gauss_blurs_3()
gauss_blurs_11()
filter2d_blurs_3()
filter2d_blurs_11()
median_blurs_3()
median_blurs_11()