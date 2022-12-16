import cv2
import numpy as np
import matplotlib.pyplot as plt

class read_display_save_class():

    def __init__(self, image_path):
        self.image_path = image_path

    def readImage(self):
        """
        readImage
        OpenCV reads in BGR, due to history.
        It follows old windows desktop colouring, which followed BGR
        """
        image= cv2.imread(self.image_path)
        return image

    # Visualize Image
    def visualize(self,image):
        plt.imshow(image)
        plt.show()

    # Convert Image of BGR to RGB
    def ConvertImageBGR2RGB(self,imageInBGR):
        imageBGR2RGB=cv2.cvtColor(imageInBGR, cv2.COLOR_BGR2RGB)
        return imageBGR2RGB