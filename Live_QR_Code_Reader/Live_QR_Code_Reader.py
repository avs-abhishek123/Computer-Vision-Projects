import cv2
from pyzbar import pyzbar

# Open video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR codes in the frame
    qr_codes = pyzbar.decode(gray)

    # Iterate over detected QR codes
    for qr_code in qr_codes:
        # Extract the QR code data
        qr_data = qr_code.data.decode('utf-8')
        qr_type = qr_code.type

        # Draw a bounding box around the QR code
        (x, y, w, h) = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw the QR code data and type on the frame
        text = f"{qr_type}: {qr_data}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Live QR Code Reader", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
