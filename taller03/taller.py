import sys
import time
import random
import cv2 as cv
import numpy as np

def main(argv):

    if len(argv) < 2:
        print('-----ATENCION-----')
        print('Revisar archivo ReadME.md para conocer los tipos de parametros permitidos...')
        return -1
    
    # Load the image
    filename = argv[0]
    src = cv.imread(filename)

    # Revisar lectura correcta de imagen
    if src is None:
        print('Error abriendo la imagen!')
        print(
            'Usage: pyramids.py [image_name -- default ../data/chicky_512.png] \n')
        return -1
    
    # Obtener dimensiones de la imagen
    height = src.shape[0]
    width = src.shape[1]


    # Revisar coordenadas ingresadas
    if len(argv) == 4:
        if int(argv[1]) > height or int(argv[1]) < 0:
            print('Error: La coordenada en Y supera la altura de la imagen o es negativo...')
            print('Altura de la Imagen        : ',height)
            return -1
        
        if int(argv[2]) > width or int(argv[2]) < 0:
            print('Error: La coordenada en X supera el ancho de la imagen o es negativo...')
            print('Anchura de la Imagen       : ',width)
            return -1
    
    return argv

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

def segmentacion(img, seed, tolerancia):
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

if __name__ == "__main__":
    inputData = main(sys.argv[1:])
    filename = inputData[0]
    img = cv.imread(filename,0)
    if(len(inputData)== 4):
        semilla=[int(inputData[2]), int(inputData[1])]
        tolerancia = int(inputData[3])
    if(len(inputData) == 2):
        height = img.shape[0]
        width = img.shape[1]
        semilla = [random.randint(0, width), random.randint(0, height)]
        print('semilla: ' +str(semilla[1])+', '+str(semilla[0]))
        tolerancia = int(inputData[1])
    gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    salida = segmentacion(gray, semilla, tolerancia)
    cv.imwrite('salida.jpg', salida)  
    cv.waitKey()
    cv.destroyAllWindows()