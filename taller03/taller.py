import sys
import cv2 as cv
import numpy as np
import functions as func


def main(argv):

    if len(argv) < 4:
        print('-----ATENCION-----')
        print('Ingresar los parametros indicados')
        print('[imagen] [coordnadaX] [coordenadaY] [Tolerancia] ')
        print('Ejemplo: Python3 main.py foto1.jpg 100 150  7')
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
    
    ### Obtener dimensiones de la imagen
    height = src.shape[0]
    width = src.shape[1]


    # Revisar parametros ingresados
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
    tolerancia = int(inputData[3])
    img = cv.imread(filename,0)
    semilla=[int(inputData[2]), int(inputData[1])]
    gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)

    cv.imshow('Input', gray) 
    salida = func.region_growing(gray, semilla, tolerancia)
    cv.imshow('Region Growing', salida)  
    cv.waitKey()
    cv.destroyAllWindows()