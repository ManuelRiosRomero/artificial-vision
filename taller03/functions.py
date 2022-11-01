import sys
import time
import cv2 as cv
import numpy as np


def vecinos(x, y, shape):
    salida = []
    maxx = shape[1]-1
    maxy = shape[0]-1
    
    #top-left
    salidax = min(max(x-1,0),maxx)
    saliday = min(max(y-1,0),maxy)
    salida.append((salidax,saliday))
    
    #top-center
    salidax = x
    saliday = min(max(y-1,0),maxy)
    salida.append((salidax,saliday))
    
    #top-right
    salidax = min(max(x+1,0),maxx)
    saliday = min(max(y-1,0),maxy)
    salida.append((salidax,saliday))
    
    #center-left
    salidax = min(max(x-1,0),maxx)
    saliday = y
    salida.append((salidax,saliday))
    
    #center-right
    salidax = min(max(x+1,0),maxx)
    saliday = y
    salida.append((salidax,saliday))
    
    #bottom-left
    salidax = min(max(x-1,0),maxx)
    saliday = min(max(y+1,0),maxy)
    salida.append((salidax,saliday))
    
    #bottom-center
    salidax = x
    saliday = min(max(y+1,0),maxy)
    salida.append((salidax,saliday))
    
    #bottom-right
    salidax = min(max(x+1,0),maxx)
    saliday = min(max(y+1,0),maxy)
    salida.append((salidax,saliday))
    
    return salida



def region_growing(img, seed, tolerancia):
    semillas2 = []
    imagenSalida = np.zeros_like(img)
    semillas2.append((seed[0], seed[1]))
    processed = []
    while(len(semillas2) > 0):
        pix = semillas2[0]
        imagenSalida[pix[0], pix[1]] = 255
        intensidad = img[seed[0], seed[1]]
        for lados in vecinos(pix[0], pix[1], img.shape):      
            promedio = homogeniedad(img, lados[0], lados[1], img.shape)
            if abs(int(promedio - intensidad)) <= tolerancia :
                imagenSalida[lados[0], lados[1]] = 255
                if not lados in processed:
                    semillas2.append(lados)
                processed.append(lados)
        semillas2.pop(0)
        cv.imshow("Proceso en Vivo",imagenSalida)
        cv.waitKey(1)
    return imagenSalida

def homogeniedad(img, x, y, shape):
    maxx = shape[1]-1
    maxy = shape[0]-1
    prom = 0
    #top-center
    if y+1 <= maxy:
        prom = prom + img[x, y+1]  
    
    #top-right
    if y+1 <= maxy and x+1 <=maxx:
        prom = prom + img[x+1, y+1]
    
    #top-left
    if y+1 <= maxy and x-1 >= 0:
        prom = prom + img[x-1, y+1]
    
    #mid-left
    if x-1 >= 0:
        prom = prom + img[x-1, y]
    
    #mid-left
    if x+1 <= maxx:
        prom = prom + img[x+1, y]

    #bottom-left
    if y-1 >= 0 and x-1 >= 0:
        prom = prom + img [x-1,y-1]

    #bottom-center
    if y-1 >= 0 :
        prom = prom + img [x, y-1]

    #bottom-right
    if y-1 >= 0 and x+1 <= maxx:
        prom = prom + img [x+1, y-1]

    return prom//8
