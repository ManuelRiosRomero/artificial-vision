
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------


def notch_reject_filter(shape, d0=9, u_k=0, v_k=0):
    P, Q = shape
    # Initialize filter with zeros
    H = np.zeros((P, Q))

    # Traverse through filter
    for u in range(0, P):
        for v in range(0, Q):
            # Get euclidean distance from point D(u,v) to the center
            D_uv = np.sqrt((u - P / 2 + u_k) ** 2 + (v - Q / 2 + v_k) ** 2)
            D_muv = np.sqrt((u - P / 2 - u_k) ** 2 + (v - Q / 2 - v_k) ** 2)

            if D_uv <= d0 or D_muv <= d0:
                H[u, v] = 0.0
            else:
                H[u, v] = 1.0

    return H
# -----------------------------------------------------


img = cv2.imread('e.jpg', 0)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
phase_spectrumR = np.angle(fshift)
magnitude_spectrum = 20*np.log(np.abs(fshift))

img_shape = img.shape

h = []
for i in range(100):
    h.append(notch_reject_filter(img_shape, 6, i+30, 0))


x = 1
for i in range(100):
    x *= h[i]
#H1 = notch_reject_filter(img_shape, 6, 9, 25)
#H2 = notch_reject_filter(img_shape, 8, -25, 39)
#H3 = notch_reject_filter(img_shape, 2, 80, 30)
#H4 = notch_reject_filter(img_shape, 2, -82, 28)

NotchFilter = x
NotchRejectCenter = fshift * NotchFilter
NotchReject = np.fft.ifftshift(NotchRejectCenter)
# Compute the inverse DFT of the result
inverse_NotchReject = np.fft.ifft2(NotchReject)


Result = np.abs(inverse_NotchReject)

plt.subplot(222)
plt.imshow(img, cmap='gray')
plt.title('Original')

plt.subplot(221)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('magnitude spectrum')

plt.subplot(223)
plt.imshow(magnitude_spectrum*NotchFilter, "gray")
plt.title("Notch Reject Filter")

plt.subplot(224)
plt.imshow(Result, "gray")
plt.title("Result")


plt.show()
