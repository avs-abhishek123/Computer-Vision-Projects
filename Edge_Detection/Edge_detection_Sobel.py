import cv2
import numpy as np
from PIL import Image, ImageFilter

# Read the original image
img = cv2.imread('images/tiger.jpg',flags=0)

img_u8 = img.astype(np.uint8)

# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_u8,(3,3), 0, 0)

# The Sobel Operator detects edges that are marked by sudden changes in pixel intensity,

"""
edges can be detected in areas where the gradient is higher than a particular threshold value. 
In addition, a sudden change in the derivative will reveal a change in the pixel intensity as well. 
With this in mind, we can approximate the derivative, using a 3×3 kernel. We use one kernel to 
detect sudden changes in pixel intensity in the X direction, and another in the Y direction. 
"""

# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# print(cv2.getBuildInformation())
# Display Sobel Edge Detection Images
# cv2.imshow('Sobel X', sobelx)
# cv2.waitKey(0)
 
# cv2.imshow('Sobel Y', sobely)
# cv2.waitKey(0)
 
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# cv2.waitKey(0)

opencv_imageX = sobelx
opencv_imageY = sobely
opencv_imageXY = sobelxy

# Notice the COLOR_BGR2RGB which means that the color is
# converted from BGR to RGB
color_covertedX = cv2.cvtColor(opencv_imageX.astype(np.uint8), cv2.COLOR_BGR2RGB)
pil_imageX = Image.fromarray(color_covertedX)
pil_imageX.save(r"output/Edge_Sample_SobelX.png")

color_covertedY = cv2.cvtColor(opencv_imageY.astype(np.uint8), cv2.COLOR_BGR2RGB)
pil_imageY = Image.fromarray(color_covertedY)
pil_imageY.save(r"output/Edge_Sample_SobelY.png")

color_covertedXY = cv2.cvtColor(opencv_imageXY.astype(np.uint8), cv2.COLOR_BGR2RGB)
pil_imageXY = Image.fromarray(color_covertedXY)
pil_imageXY.save(r"output/Edge_Sample_SobelXY.png")