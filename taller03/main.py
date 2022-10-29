import sys
import cv2 as cv
import numpy as np
import functions as func

def main(argv):

    if len(argv) < 3:
        print('-----ATENCION-----')
        print('Ingresar los parametros indicados')
        print('Parametros: imagen coordenadaY coordenadaX')
        print('Ejemplo: Python3 main.py foto1.jpg 100 150')
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
    #dimensions = src.shape
    height = src.shape[0]
    width = src.shape[1]
    #channels = src.shape[2]
    
    """ 
    print('Dimensiones de la Imagen   : ',dimensions) 
    print('Canales de la iamgen       : ',channels)
    """

    # Revisar coordenadas ingresadas a la imagen
    if int(argv[1]) > height or int(argv[1]) < 0:
        print('Error: La coordenada en Y supera la altura de la imagen o es negativo...')
        print('Altura de la Imagen        : ',height)
        return -1
    
    if int(argv[2]) > width or int(argv[2]) < 0:
        print('Error: La coordenada en X supera el ancho de la imagen o es negativo...')
        print('Anchura de la Imagen       : ',width)
        return -1

    return argv

if __name__ == "__main__":
    inputData = main(sys.argv[1:])
    filename = inputData[0]
    img = cv.imread(filename,0)
    semilla=[int(inputData[1]), int(inputData[2])]
    ret, imgBN = cv.threshold(img, 130, 255, cv.THRESH_BINARY)

    cv.imshow('Input', imgBN)
    salida = func.region_growing(imgBN, semilla)

    cv.imshow('Region Growing', salida)
    cv.waitKey()
    cv.destroyAllWindows()

