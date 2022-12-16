import cv2
import mediapipe as mp
import time

class webcam_video_capture:
    self.pTime = 0

    def VideoCapture():
        """
        """
        cap = cv2.VideoCapture(0)

        while True:
            """
            read():
                read() returns boolean and data.
                If there are not 2 variables,
                a tuple will be assigned to one variable.
                The boolean is mostly used for error catching. 
                Assigning a tuple to 1 var with 2 data items can sometimes be useful, 
                but in this instance, you should create 2 vars 
                and split the data into 2 variables to make it easier.
            """
            success, img = cap.read()
            # openCV reads in BGR by default, so need to convert to rgb
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img = img,
                        text = f'FPS Display',
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
            cv2.imshow("Test", img)
            # Display Video and when 'q'
            # is entered, destroy the window
            if cv2.waitKey(1) & 0xff == ord('q'):
                break