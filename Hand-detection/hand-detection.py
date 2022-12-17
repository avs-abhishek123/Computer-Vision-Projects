from read_display_save import read_display_save_class as rds_img
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "images\\Wednesday-2.jpg"
# https://stackoverflow.com/questions/32302180/typeerror-image-data-can-not-convert-to-float

rds_img_object = rds_img(image_path)

def detect_faces(image):
    #converted to grayscale 
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # flipped_gray_image = cv2.flip(gray_img, 1)

    #Training Face Data using Cascade Classifier 
    trained_face_data = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    # trained_face_data = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')

    #grayscale converted
    face_coordinates = trained_face_data.detectMultiScale(gray_img)


    print(face_coordinates)

    for coordinate in face_coordinates:
        (x, y, w, h) = coordinate
        colors = np.random.randint(1, 255, 3)
        cv2.rectangle(image, (x, y), (x + w, y + h), (int(colors[0]), int(colors[1]), int(colors[2])), thickness=2)
    return image


# Reading image using readImage() function
BGR_Image= rds_img_object.readImage()
rds_img_object.visualize(BGR_Image)

# Reading image using ConvertImageBGR2RGB() function
image = rds_img_object.ConvertImageBGR2RGB(BGR_Image)

# Displaying image using visualize() function
rds_img_object.visualize(image)
print("------------------------------------------------------------")

print("FACE DETECTION USING HAAR CASCADE CLASSIFIER")

# Reading image using visualize() function
x=detect_faces(image)
print("------------------------------------------------------------")
# Displaying image using visualize() function
rds_img_object.visualize(x) 