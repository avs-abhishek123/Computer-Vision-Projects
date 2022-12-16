import cv2
import mediapipe as mp
import time

"""
Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])

Parameters:
img: It is the image on which text is to be drawn.
text: Text string to be drawn.
org: It is the coordinates of the bottom-left corner of the text string in the image. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
fontFace: It denotes the type of font you want to use. OpenCV supports only a subset of Hershey Fonts.
    FONT_HERSHEY_SIMPLEX
    FONT_HERSHEY_PLAIN
    FONT_HERSHEY_DUPLEX
    FONT_HERSHEY_COMPLEX
    FONT_HERSHEY_TRIPLEX
    FONT_HERSHEY_COMPLEX_SMALL
    FONT_HERSHEY_SCRIPT_SIMPLEX
    FONT_HERSHEY_SCRIPT_COMPLEX
    FONT_ITALIC
fontScale: Font scale factor that is multiplied by the font-specific base size.
color: It is the color of text string to be drawn. For BGR, we pass a tuple. eg: (255, 0, 0) for blue color.
thickness: It is the thickness of the line in px.
lineType: This is an optional parameter.It gives the type of the line to be used.
bottomLeftOrigin: This is an optional parameter. When it is true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.

Return Value: It returns an image.

https://www.askpython.com/python-modules/opencv-puttext
"""

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils



while True:
    pTime = time.time()
    # cTime = 0
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img = img,
                text = f'Hand Tracking System',
                org = (140, 40),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 1,
                color = (255, 255, 255),
                thickness = 2 )
    cv2.putText(img = img,
                text = f'FPS: {int(fps)}',
                org = (20, 60),
                fontFace = cv2.FONT_HERSHEY_PLAIN,
                fontScale = 1,
                color = (255,0,255),
                thickness = 1)

    cv2.imshow("Image", img)

    # Display Video and when 'q'
    # is entered, destroy the window
    if cv2.waitKey(1) & 0xff == ord('q'):
        break