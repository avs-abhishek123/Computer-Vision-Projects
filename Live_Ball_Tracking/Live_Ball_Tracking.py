import cv2
import numpy as np

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Set the lower and upper boundaries for the ball color in HSV format
lower_color = np.array([0, 100, 100])
upper_color = np.array([10, 255, 255])

while True:
    # Read the frame from the video capture
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask based on the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Perform morphological operations to remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the ball position
    ball_pos = None

    if len(contours) > 0:
        # Find the contour with the largest area (the ball)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the centroid of the contour
        M = cv2.moments(largest_contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            ball_pos = (cx, cy)

            # Draw a circle at the ball position
            cv2.circle(frame, ball_pos, 10, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Ball Tracking", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
