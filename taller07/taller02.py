import sys
import cv2 as cv
import numpy as np


def main(argv):
    print("""
    Zoom In-Out demo
    ------------------
    * [i] -> Zoom [i]n
    * [o] -> Zoom [o]ut
    * [ESC] -> Close program
    """)

    filename = argv[0] if len(argv) > 0 else 'a.jpg'
    # Load the image
    src = cv.imread(cv.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print(
            'Usage: pyramids.py [image_name -- default ../data/chicky_512.png] \n')
        return -1

    #src = cv.pyrUp(src, dstsize=(2 * cols, 2 * rows))
    src = down_scale(src, "nivel-1.jpg")
    src = down_scale(src, "nivel-2.jpg")
    src = down_scale(src, "nivel-3.jpg")
    print('** Zoom In: Image x 2')

    return 0


def down_scale(src, title):
    src = gaussSmallerLayer(src)
    src = processImage(src)
    cv.imwrite(title, src)
    return src


def gaussSmallerLayer(src):
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float64)
    kernel = np.float64([[1/256, 4/256, 6/256, 4/256, 1/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [6/256, 24/256, 36/256, 24/256, 6/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [1/256, 4/256, 6/256, 4/256, 1/256]])
    dst = cv.filter2D(src, -1, kernel)
    return(dst)


def processImage(image="a.jpg"):
    new_image = []
    print(type(image))
    for i in range(len(image)):
        new_row = []
        for j in range(len(image)):
            if i % 2 != 0 and j % 2 != 0:
                new_row.append(image[i][j])
        if new_row:
            new_image.append(np.array(np.array(new_row)))
    return np.array(new_image)


if __name__ == "__main__":
    main(sys.argv[1:])
