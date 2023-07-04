
# import cv2

# # Global variables to store the coordinates of mouse clicks
# click_x = []
# click_y = []
# draw_box = False

# # Constants for YOLO format
# image_width = 640
# image_height = 640

# # Counter for image and label filenames
# counter = 0

# # Mouse callback function
# def mouse_callback(event, x, y, flags, param):
#     global click_x, click_y, draw_box

#     if event == cv2.EVENT_LBUTTONDOWN:
#         click_x.append(x)
#         click_y.append(y)
#         if len(click_x) == 2:
#             draw_box = True

# # Create a window and set the mouse callback function
# cv2.namedWindow('Manual Labeling')
# cv2.setMouseCallback('Manual Labeling', mouse_callback)

# # Initialize video capture
# cap = cv2.VideoCapture(0)

# while True:
#     # Read frame from video capture
#     ret, frame = cap.read()

#     if draw_box:
#         # Draw the detection box
#         xmin = min(click_x)
#         ymin = min(click_y)
#         xmax = max(click_x)
#         ymax = max(click_y)

#         # Calculate normalized coordinates
#         x_center = (xmin + xmax) / (2 * image_width)
#         y_center = (ymin + ymax) / (2 * image_height)
#         width = (xmax - xmin) / image_width
#         height = (ymax - ymin) / image_height

#         # Save the image
#         image_filename = f'image_{counter}.jpg'
#         cv2.imwrite(image_filename, frame)

#         # Write the label in YOLO format to a text file
#         label_filename = f'label_{counter}.txt'
#         with open(label_filename, 'w') as f:
#             f.write(f"0 {x_center} {y_center} {width} {height}\n")

#         # Increment the counter
#         counter += 1

#         # Clear the click coordinates and reset the drawing flag
#         click_x.clear()
#         click_y.clear()
#         draw_box = False

#     # Display the frame
#     cv2.imshow('Manual Labeling', frame)

#     # Exit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()

import cv2

# Global variables to store the coordinates of mouse clicks
click_x = []
click_y = []
draw_box = False
dataset_path = "C:/Users/HP/Desktop/Computer-Vision-Projects/Manual_labelling/generated_dataset"
# Constants for YOLO format
image_width = 640
image_height = 640

# Counter for image and label filenames
counter = 0

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global click_x, click_y, draw_box

    if event == cv2.EVENT_LBUTTONDOWN:
        click_x.append(x)
        click_y.append(y)
        if len(click_x) == 2:
            draw_box = True

# Create a window and set the mouse callback function
cv2.namedWindow('Manual Labeling')
cv2.setMouseCallback('Manual Labeling', mouse_callback)

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()

    if draw_box:
        # Draw the detection box
        xmin = min(click_x)
        ymin = min(click_y)
        xmax = max(click_x)
        ymax = max(click_y)

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Manual Labeling', frame)

    if draw_box:
        # Calculate normalized coordinates
        x_center = (xmin + xmax) / (2 * image_width)
        y_center = (ymin + ymax) / (2 * image_height)
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height

        # Save the image
        image_filename = f'{dataset_path}/images/image_{counter}.jpg'
        cv2.imwrite(image_filename, frame)

        # Write the label in YOLO format to a text file
        label_filename = f'{dataset_path}/labels/label_{counter}.txt'
        with open(label_filename, 'w') as f:
            # Rest of your code for writing labels to the file
            f.write(f"0 {x_center} {y_center} {width} {height}\n")

        # Increment the counter
        counter += 1

        # Clear the click coordinates and reset the drawing flag
        click_x.clear()
        click_y.clear()
        draw_box = False

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
