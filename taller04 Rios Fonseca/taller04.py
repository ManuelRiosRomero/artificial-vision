import sys
import cv2 as cv
import numpy as np

def main(argv):
    if len(argv) < 1:
        print('-----ATENCION-----')
        print('Ingrese el nombre del archivo a leer')
        print('python3 taller04.py [img source]')
        return -1

    # Load the image
    filename = argv[0]
    src = cv.imread(filename, cv.IMREAD_GRAYSCALE)

    # Revisar lectura correcta de imagen
    if src is None:
        print('Error abriendo la imagen!')
        pr+int(
            'Usage: pyramids.py [image_name -- default ../data/chicky_512.png] \n')
        return -1
    gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    return src

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

# def caracterizacion(img):
#     etiqueta = 255
#     tamano = img.size
#     height = img.shape[0]
#     width = img.shape[1]
#     salida = np.zeros_like(img)
#     semillas2 = []
#     semillas2.append((0,0))
#     processed = []
#     while(tamano > 0):
#         print("Antes del pix")
#         pix = semillas2[0]
#         salida[pix[0], pix[1]] = 255
#         for x in range(width):
#             for y in range(height):
#                 for lados in vecinos(pix[0], pix[1], img.shape):
#                     if not lados in processed:
#                         semillas2.append(lados)
#                     processed.append(lados)      
#                     if img[lados[0],lados[1]] == 255:
#                         salida[lados[0], lados[1]] = 255
#                 cv.imshow("Proceso en Vivo",salida)
#                 cv.waitKey(1)
#             semillas2.pop(0)

#     return salida

def caracterizacion(img):
    etiqueta = 255
    tamano = img.size
    height = img.shape[0]
    width = img.shape[1]
    salida = np.zeros_like(img)
    cola = []
    processed = []

    for x in range(width):
        for y in range(height):
            if img[x,y] > 0:
                for lados in vecinos(x,y, img.shape):
                    if img[lados[0],lados[1]] == 255:
                        cola.append((lados[0],lados[1]))
    while(len(cola)>0):
        pix = cola[0]
        #salida[pix[0], pix[1]] = 255
        for lados in vecinos(pix[0], pix[1], img.shape):
            if not lados in processed:
                processed.append(lados)    
                salida[lados[0], lados[1]] = etiqueta
            cv.imshow("Proceso en Vivo",salida)
            cv.waitKey(1)
        cola.pop(0)
        etiqueta = etiqueta-1
    return salida



if __name__ == "__main__":
    img = main(sys.argv[1:])
    ret, binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    # cv.imshow("Imagen Leida", img)
    # cv.imshow("imagen binaria", binary)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # out = segmentacion(binary)
    
    out = caracterizacion(img)
    cv.imshow("imagen final",out)
    cv.waitKey(0)
    cv.destroyAllWindows()

