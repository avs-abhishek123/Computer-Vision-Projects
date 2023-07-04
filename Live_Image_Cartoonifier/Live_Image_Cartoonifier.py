import cv2

def cartoonify(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce noise
    blur = cv2.medianBlur(gray, 5)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter to smooth the image while keeping edges sharp
    filtered = cv2.bilateralFilter(image, 9, 250, 250)

    # Combine the filtered image with edges using bitwise AND
    cartoon = cv2.bitwise_and(filtered, filtered, mask=edges)

    return cartoon

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from webcam
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        break

    # Apply cartoonify function to the frame
    cartoon = cartoonify(frame)

    # Display the original and cartoonified frames
    cv2.imshow("Original", frame)
    cv2.imshow("Cartoonified", cartoon)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy windows
cap.release()
cv2.destroyAllWindows()
