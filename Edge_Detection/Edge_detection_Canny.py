# The algorithm itself follows a three-stage process for extracting edges from an image. 
# Add to it image blurring, a necessary preprocessing step to reduce noise. 
# This makes it a four-stage process, which includes:
"""
1. Noise Reduction
2. Calculating Intensity Gradient of the Image
3. Suppression of False Edges
4. Hysteresis Thresholding
"""
import cv2
from PIL import Image, ImageFilter
import numpy as np
# Read the original image
img = cv2.imread('images/tiger.jpg',flags=0)

img_u8 = img.astype(np.uint8)

# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_u8,(3,3), 0, 0)
# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) 
opencv_image = edges
# Display Canny Edge Detection Image
# cv2.imshow('Canny Edge Detection', edges)
# cv2.waitKey(0)

# Notice the COLOR_BGR2RGB which means that the color is
# converted from BGR to RGB
color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(color_coverted)
pil_image.save(r"output/Edge_Sample_Canny.png")
