import cv2
import time

cap = cv2.VideoCapture(0)
pTime = 0
"""
Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])

Parameters:
image: It is the image on which text is to be drawn.
text: Text string to be drawn.
org: It is the coordinates of the bottom-left corner of the text string in the image. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
font: It denotes the font type. Some of font types are FONT_HERSHEY_SIMPLEX, FONT_HERSHEY_PLAIN, , etc.
fontScale: Font scale factor that is multiplied by the font-specific base size.
color: It is the color of text string to be drawn. For BGR, we pass a tuple. eg: (255, 0, 0) for blue color.
thickness: It is the thickness of the line in px.
lineType: This is an optional parameter.It gives the type of the line to be used.
bottomLeftOrigin: This is an optional parameter. When it is true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.

Return Value: It returns an image.
"""

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'Hand Tracking System', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 )
    cv2.putText(img, f'FPS:{int(fps)}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Test", img)
    # Display Video and when 'q'
    # is entered, destroy the window
    if cv2.waitKey(1) & 0xff == ord('q'):
        break