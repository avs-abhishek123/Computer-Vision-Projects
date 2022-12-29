import numpy as np
import cv2

# https://theailearner.com/2021/09/25/harris-corner-detection/

# Load the image and convert to grayscale
img = cv2.imread('images/chessboard.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find Harris corners as we did in the previous blog
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop. We stop it after a specified number of iterations
# or a certain accuracy is achieved, whichever occurs first.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

# Refine the corners using cv2.cornerSubPix()
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# To display, first convert the centroids and corners to integer
centroids = np.int0(centroids)
corners = np.int0(corners)

# then i have used red color to mark Harris Corners
# and green color to mark refined corners
img[centroids[:,1], centroids[:,0]]=[0,0,255]
img[corners[:,1], corners[:,0]] = [0,255,0]

# Write the image at the desired location
cv2.imwrite('output/corner_detection/subpixel5.png',img)