import cv2
import numpy as np

# Read image
original_image = cv2.imread('color_wheel_2.jpg', cv2.IMREAD_UNCHANGED)

# Obtain original size

original_size = original_image.shape
original_height = original_size[0]
original_width = original_size[1]

# extract channels
red_channel = original_image[:, :, 2]
green_channel = original_image[:, :, 1]
blue_channel = original_image[:, :, 0]

# create empty image with same shape as that of original image
red_img = np.zeros(original_size)
blue_img = np.zeros(original_size)
green_img = np.zeros(original_size)

# assign the each channel of original image to empty image
red_img[:, :, 2] = red_channel
blue_img[:, :, 0] = blue_channel
green_img[:, :, 1] = green_channel

# save image
cv2.imwrite('color_wheel_2_R.jpg', red_img)
cv2.imwrite('color_wheel_2_G.jpg', green_img)
cv2.imwrite('color_wheel_2_B.jpg', blue_img)

# ---------------------------------- Rezise images ------------------------------------------------------

# percent by which the image is resized 0.75, 0.5, 0.25
scale_percent_R = 75
scale_percent_G = 50
scale_percent_B = 25


# calculate the percent of original dimensions
width_R = int(red_img.shape[1] * scale_percent_R / 100)
height_R = int(red_img.shape[0] * scale_percent_R / 100)

width_G = int(green_img.shape[1] * scale_percent_G / 100)
height_G = int(green_img.shape[0] * scale_percent_G / 100)

width_B = int(blue_img.shape[1] * scale_percent_B / 100)
height_B = int(blue_img.shape[0] * scale_percent_B / 100)

# dsize
dsize_R = (width_R, height_R)
dsize_G = (width_G, height_G)
dsize_B = (width_B, height_B)
dsize_original = (original_width, original_height)

# resize image
reds_img = cv2.resize(red_img, dsize_R)
greens_img = cv2.resize(green_img, dsize_G)
blues_img = cv2.resize(blue_img, dsize_B)


cv2.imwrite('color_wheel_2_sR.jpg', reds_img)
cv2.imwrite('color_wheel_2_sG.jpg', greens_img)
cv2.imwrite('color_wheel_2_sB.jpg', blues_img)


# ------------------------------------------ Go back to original size ---------------------------

redss_img = cv2.resize(reds_img, dsize_original)
greenss_img = cv2.resize(greens_img, dsize_original)
bluess_img = cv2.resize(blues_img, dsize_original)


cv2.imwrite('color_wheel_2_ssR.jpg', redss_img)
cv2.imwrite('color_wheel_2_ssG.jpg', greenss_img)
cv2.imwrite('color_wheel_2_ssB.jpg', bluess_img)

# ------------------------------------------ Merge    ---------------------------

redss_channel = redss_img[:, :, 2]
greenss_channel = greenss_img[:, :, 1]
bluess_channel = bluess_img[:, :, 0]

merged = cv2.merge([bluess_channel, greenss_channel, redss_channel])


cv2.imwrite('merged.jpg', merged)


# ----------------------------------------- Substract ---------------------------------
im1 = cv2.imread('color_wheel_2.jpg', cv2.IMREAD_UNCHANGED)
im2 = cv2.imread('merged.jpg', cv2.IMREAD_UNCHANGED)

sub = cv2.subtract(im1, im2)

cv2.imwrite('final.jpg', sub)
