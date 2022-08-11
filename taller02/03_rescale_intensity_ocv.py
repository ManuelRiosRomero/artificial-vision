# Call the required package
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys


def convert(img, bits):
    return np.uint8(img/bits) * bits


if len(sys.argv) != 3:
    sys.exit(
        "Please insert correct number of parameters. python <file_name> <image_name> <bits>")

image_name = sys.argv[1]
bits = int(sys.argv[2])

# Read the information of the original image
img0 = cv2.imread(image_name)  # Read images


blue_img, green_img, red_img = cv2.split(img0)

operator = 0

if bits == 8:
    operator = 4
elif bits == 6:
    operator = 16
elif bits == 4:
    operator = 32
elif bits == 2:
    operator = 64
elif bits == 1:
    operator = 128

if operator == 0:
    sys.exit("Wrong number of bits")

red_m = convert(red_img, operator)
blue_m = convert(blue_img, operator)
green_m = convert(green_img, operator)
merged = cv2.merge([blue_m, green_m, red_m])

cv2.imwrite('blue.png', red_m)
cv2.imwrite('red.png', blue_m)
cv2.imwrite('green.png', green_m)
cv2.imwrite('merged.png', merged)


# Display the resulting image
title = [' red image', ' blue image',
         ' green image', "merged"]  # Subgraph title
imgs = [red_m, blue_m, green_m, merged]


for i in range(len(imgs)):
    plt.subplot(2, 3, i + 1)  # python List from 0 Start counting , So here i+1
    plt.imshow(imgs[i], 'gray')
    plt.title(title[i])
    plt.xticks([]), plt.yticks([])
    plt.savefig('combine.jpg')
    plt.show()
