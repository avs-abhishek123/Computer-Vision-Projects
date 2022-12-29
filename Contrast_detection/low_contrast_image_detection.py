import cv2
from skimage.exposure import is_low_contrast

# Read the image
img = cv2.imread('images/low_contrast.png')

# Check if it is low contrast or not
out = is_low_contrast(img, fraction_threshold=0.3)

# if true print low contrast otherwise high contrast
if out:
    print('Image has low contrast')
else:
    print('Image has high contrast')