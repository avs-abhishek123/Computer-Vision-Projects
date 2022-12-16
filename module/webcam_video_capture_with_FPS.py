import cv2
import mediapipe as mp
import time

class webcam_video_capture_class:

    def __init__(self, display_window_text= "Test"):
        self.display_window = display_window_text
        # "display_window_text = Test"

    def FPS(self, prev_frame_time):

        # time when we finish processing for this frame
        new_frame_time = time.time()

        # Calculating the fps
        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate result
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        return fps, prev_frame_time

    def display(self, img):
        cv2.imshow(self.display_window, img)

    def VideoCapture(self):
        """
        opens web cam & displays the fps while capturing image
        """
        new_frame_time = 0
        prev_frame_time = 0
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

                https://stackoverflow.com/questions/64692479/cv2-videocapture0-read-returns-false-none
            """
            success, img = cap.read()

            # openCV reads in BGR by default, so need to convert to rgb
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            fps, prev_frame_time = self.FPS(prev_frame_time)

            print("FPS:",fps)

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
            cv2.putText(img = img,
                        text = f'FPS Display',
                        org = (20, 40),
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

            self.display(img)

            # Display Video and when 'q'
            # is entered, destroy the window
            # pTime = 0
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
