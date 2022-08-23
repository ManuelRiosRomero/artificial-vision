
import cv2 as cv
import numpy as np
#  Global Variables
MAX_KERNEL_LENGTH = 7
    # Applying Homogeneous blur
def homo_func(img):
    for i in range(1, MAX_KERNEL_LENGTH, 2):
        dst = cv.blur(img, (i, i))
    return dst
    
    # Applying Gaussian blur
def gauss_func(img):
    for i in range(1, MAX_KERNEL_LENGTH, 2):
        dst = cv.GaussianBlur(img, (i, i), 0)
    return dst

    
    # Applying Median blur
def median_func(img):    
    for i in range(1, MAX_KERNEL_LENGTH, 2):
        dst = cv.medianBlur(img, i)
    return dst
    
    # Applying Bilateral Filter
def bilat_func(img):
    for i in range(1, MAX_KERNEL_LENGTH, 2):
        dst = cv.bilateralFilter(img, i, i * 2, i / 2)
    return dst

def filter2D_r1_func(img):   
    kernel_size=3    
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
    kernel=np.float32([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    #kernel /= (kernel_size * kernel_size)
    dst = cv.filter2D(img, -1, kernel)
    return(dst)

def filter2D_r2_func(img):   
    kernel_size=5    
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
    kernel=np.float32([[-1,-1,-1,-1,-1],[-1,2,2,2,-1],[-1,2,8,2,-1],[-1,2,2,2,-1],[-1,-1,-1,-1,-1]])
    #kernel /= (kernel_size * kernel_size)
    dst = cv.filter2D(img, -1, kernel)
    return(dst)

def filter2D_p_func(img):   
    kernel_size=3    
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
    kernel=np.float32([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
    #kernel /= (kernel_size * kernel_size)
    dst = cv.filter2D(img, -1, kernel)
    return(dst)

def filtros_function(img):
    dst=filter2D_p_func(img)
    dst=filter2D_p_func(dst)
    dst=filter2D_p_func(dst)
    dst=filter2D_p_func(dst)
    

    dst=bilat_func(dst)
    dst=bilat_func(dst)
    dst=bilat_func(dst)
    dst=bilat_func(dst)
    dst=bilat_func(dst)
    dst=bilat_func(dst)
    dst=bilat_func(dst)

    #dst=median_func(dst)

    dst=filter2D_r1_func(dst)
   
    return(dst)



img = cv.imread('img.jpg', cv.IMREAD_UNCHANGED)
fil=filtros_function(img)
cv.imwrite('fil.jpg', fil)
    