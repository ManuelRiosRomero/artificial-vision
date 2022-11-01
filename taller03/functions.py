import sys
import cv2 as cv
import numpy as np
import time

def get8n(x, y, shape):
    out = []
    maxx = shape[1]-1
    maxy = shape[0]-1
    
    #top left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    
    #top center
    outx = x
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    
    #top right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    
    #left
    outx = min(max(x-1,0),maxx)
    outy = y
    out.append((outx,outy))
    
    #right
    outx = min(max(x+1,0),maxx)
    outy = y
    out.append((outx,outy))
    
    #bottom left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))
    
    #bottom center
    outx = x
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))
    
    #bottom right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))
    
    return out



def region_growing(img, seed, tolerancia):
    seed_points = []
    outimg = np.zeros_like(img)
    seed_points.append((seed[0], seed[1]))
    processed = []
    while(len(seed_points) > 0):
        pix = seed_points[0]
        outimg[pix[0], pix[1]] = 255
        intensidad = img[seed[0], seed[1]]
        for coord in get8n(pix[0], pix[1], img.shape):      
            promedio = homogeniedad(img, coord[0], coord[1], img.shape)
            if abs(int(promedio - intensidad)) <= tolerancia :
                outimg[coord[0], coord[1]] = 255
                if not coord in processed:
                    seed_points.append(coord)
                processed.append(coord)
        seed_points.pop(0)
        cv.imshow("progress",outimg)
        cv.waitKey(1)
    return outimg

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
