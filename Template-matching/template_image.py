"""
https://theailearner.com/2020/12/12/template-matching-using-opencv/
"""
import cv2

# read input and template image
img = cv2.imread('images/card.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread('images/heart.png',0)
w, h = template.shape[::-1]

# Apply template Matching
# res = cv2.matchTemplate(img_gray,template,cv2.TM_SQDIFF)
res = cv2.matchTemplate(img_gray,template,cv2.TM_SQDIFF)

# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF)
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR)
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR_NORMED)

# Find min/max value and location
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, 
# take minimum otherwise maximum
bottom_right = (min_loc[0] + w, min_loc[1] + h)

# draw the rectangle
cv2.rectangle(img,min_loc, bottom_right, (0,0,255), 2)

# Display the image
cv2.imshow('a', img)
cv2.waitKey(0)