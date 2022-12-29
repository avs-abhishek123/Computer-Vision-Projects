import numpy as np
import cv2

"""
cv2.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance, [,mask[,blockSize[,useHarrisDetector[,k]]]])

# image - Input 8-bit or floating-point 32-bit, single-channel image
# maxCorners - Maximum number of corners to return. If there are more corners than are found, the strongest of them is returned. if <= 0 implies that no limit on the maximum is set and all detected corners are returned
# qualityLevel - Parameter characterizing the minimal accepted quality of image corners. See the above paragraph for explanation
# minDistance - Minimum possible Euclidean distance between the returned corners
# mask - Optional region of interest. If the image is not empty it specifies the region in which the corners are detected
# blockSize - Size of an average block for computing a derivative covariation matrix over each pixel neighborhood
# useHarrisDetector - whether to use Shi-Tomasi or Harris Corner
# k - Free parameter of the Harris detector

https://theailearner.com/2021/09/27/shi-tomasi-corner-detector/

"""

# Read the image and convert to greyscale
img = cv2.imread('images/chessboard.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the top 20 corners using the cv2.goodFeaturesToTrack()
corners = cv2.goodFeaturesToTrack(gray,20,0.01,10)
corners = np.int0(corners)

# Iterate over the corners and draw a circle at that location
for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),5,(0,0,255),-1)
    
# Display the image
cv2.imshow('a', img)
cv2.waitKey(0)