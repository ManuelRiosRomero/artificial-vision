import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def down_scale(src, title):
    src = gaussSmallerLayer(src)
    src = processImage(src)
    cv.imwrite(title, src)
    return src

def gaussSmallerLayer(src):
    kernel_size = 3
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float64)
    kernel = np.float64([[1/256, 4/256, 6/256, 4/256, 1/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [6/256, 24/256, 36/256, 24/256, 6/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [1/256, 4/256, 6/256, 4/256, 1/256]])
    dst = cv.filter2D(src, -1, kernel)
    return(dst)

def processImage(image):
    new_image = []
    for i in range(len(image)):
        new_row = []
        for j in range(len(image)):
            if i % 2 != 0 and j % 2 != 0:
                new_row.append(image[i][j])
        if new_row:
            new_image.append(np.array(np.array(new_row)))
    return np.array(new_image)

def sobel(src):
    scale = 1
    delta = 0
    ddepth = cv.CV_16S
    
    src = cv.GaussianBlur(src, (5, 5), 0)
    
    grad_x = cv.Sobel(src, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

    grad_y = cv.Sobel(src, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    
    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad


imA= cv.imread("img_a.jpeg",0)
imB= cv.imread("img_b.jpeg",0)
imC= cv.imread("img_c.jpeg",0)
imD= cv.imread("img_d.jpeg",0)
imE= cv.imread("img_e.jpeg",0)

#GAUSS DOWN
srcA = down_scale(imA, "GaussA.jpg")
srcB = down_scale(imB, "GaussB.jpg")
srcC = down_scale(imC, "GaussC.jpg")
srcD = down_scale(imD, "GaussD.jpg")
srcE = down_scale(imE, "GaussE.jpg")

#SOBEL
kernel_size = 3
kernel = np.ones((kernel_size, kernel_size), dtype=np.float64)
#--------------------------------------#
soa=sobel(srcA)
cv.imwrite("bordeA.png",soa)
di1 = cv.dilate(soa,kernel,iterations = 1)
cv.imwrite("diA.png",di1)
sum1=cv.subtract(di1,srcA)
cv.imwrite("reA.png",sum1)
dil1 = cv.dilate(sum1,kernel,iterations = 1)
cv.imwrite("dilA.png",dil1)
#------------------------------------#
sob=sobel(srcB)
cv.imwrite("bordeB.png",sob)
di2 = cv.dilate(sob,kernel,iterations = 1)
cv.imwrite("diB.png",di2)
sum2=cv.subtract(di2,srcB)
cv.imwrite("reB.png",sum2)
dil2 = cv.dilate(sum2,kernel,iterations = 1)
cv.imwrite("dilB.png",dil2)

#----------------------------------#
soc=sobel(srcC)
cv.imwrite("bordeC.png",soc)
di3 = cv.dilate(soc,kernel,iterations = 1)
cv.imwrite("diC.png",di3)
sum3=cv.subtract(di3,srcC)
cv.imwrite("reC.png",sum3)
dil3 = cv.dilate(sum3,kernel,iterations = 1)
cv.imwrite("dilC.png",dil3)
#-----------------------------------#
sod=sobel(srcD)
cv.imwrite("bordeD.png",sod)
di4 = cv.dilate(sod,kernel,iterations = 1)
cv.imwrite("diD.png",di4)
sum4=cv.subtract(di4,srcD)
cv.imwrite("reD.png",sum4)
dil4 = cv.dilate(sum4,kernel,iterations = 1)
cv.imwrite("dilD.png",dil4)
#-----------------------------------#
soe=sobel(srcE)
cv.imwrite("bordeE.png",soe)
di5 = cv.dilate(soe,kernel,iterations = 1)
cv.imwrite("diE.png",di5)
sum5=cv.subtract(di5,srcE)
cv.imwrite("reE.png",sum5)
dil5 = cv.dilate(sum5,kernel,iterations = 1)
cv.imwrite("dilE.png",dil5)
#--------------------------------------#
#no save
#os.remove('diA.png')
#os.remove('diB.png')
#os.remove('diC.png')
#os.remove('diD.png')
#os.remove('diE.png')
#doesn't help
#os.remove('dilA.png')
#os.remove('dilB.png')
#os.remove('dilC.png')
#os.remove('dilD.png')
#os.remove('dilE.png')