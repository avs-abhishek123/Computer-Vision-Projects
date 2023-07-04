import cv2

# Global variables to store the coordinates of mouse clicks
click_x = []
click_y = []
draw_box = False

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
        draw_box = True

    elif event == cv2.EVENT_LBUTTONUP:
        click_x.append(x)
        click_y.append(y)
        draw_box = False

# Create a window and set the mouse callback function
cv2.namedWindow('Manual Labeling')
cv2.setMouseCallback('Manual Labeling', mouse_callback)

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()

    if draw_box and len(click_x) == 2:
        # Draw the detection box
        xmin = click_x[0]
        ymin = click_y[0]
        xmax = click_x[1]
        ymax = click_y[1]

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Manual Labeling', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not draw_box and len(click_x) == 2:
        # Calculate normalized coordinates
        x_center = (click_x[0] + click_x[1]) / (2 * image_width)
        y_center = (click_y[0] + click_y[1]) / (2 * image_height)
        width = (click_x[1] - click_x[0]) / image_width
        height = (click_y[1] - click_y[0]) / image_height

        # Save the image
        image_filename = f'image_{counter}.jpg'
        cv2.imwrite(image_filename, frame)

        # Write the label in YOLO format to a text file
        label_filename = f'label_{counter}.txt'
        with open(label_filename, 'w') as f:
            f.write(f"0 {x_center} {y_center} {width} {height}\n")

        # Increment the counter
        counter += 1

        # Clear the click coordinates
        click_x.clear()
        click_y.clear()

# Release resources
cap.release()
cv2.destroyAllWindows()
