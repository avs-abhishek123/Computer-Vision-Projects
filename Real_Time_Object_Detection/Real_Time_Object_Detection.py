import cv2
import numpy as np

# Load YOLO
# net = cv2.dnn.readNet("C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/yolov3.weights", "C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/yolov3.cfg")
# Load the pre-trained YOLO model
net = cv2.dnn_DetectionModel("C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/yolov3.weights", "C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/yolov3.cfg")
net.setInputSize(608, 608)  # Set the input size for the model
net.setInputScale(1.0 / 255)  # Set the input scale for the model
net.setInputSwapRB(True)  # Set the color channel order (BGR to RGB)

# Load class labels
with open("C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/coco.names", 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

# # Load class labels
# with open("C:/Users/HP/Desktop/Computer-Vision-Projects/Real_Time_Object_Detection/coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

# # Get layer names
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# # Initialize video capture
# cap = cv2.VideoCapture(0)

# while True:
#     # Capture frame from video feed
#     ret, frame = cap.read()

#     # Perform object detection
#     height, width, channels = frame.shape
#     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     # Process the detected objects
#     class_ids = []
#     confidences = []
#     boxes = []
#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 # Object detected
#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)

#                 # Calculate the top-left corner of the bounding box
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)

#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     # Apply non-maximum suppression to eliminate redundant overlapping boxes
#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

#     # Draw bounding boxes and labels on the frame
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     colors = np.random.uniform(0, 255, size=(len(classes), 3))
#     if len(indexes) > 0:
#         for i in indexes.flatten():
#             x, y, w, h = boxes[i]
#             label = classes[class_ids[i]]
#             confidence = confidences[i]
#             color = colors[i]

#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 5), font, 0.5, color, 2)

#     # Display the frame
#     cv2.imshow("Real-Time Object Detection", frame)

#     # Exit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()



# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()

    # Perform object detection
    classes, scores, boxes = net.detect(frame, confThreshold=0.5, nmsThreshold=0.4)

    # Process detection results
    if len(classes) > 0:
        for class_id, score, box in zip(classes.flatten(), scores.flatten(), boxes):
            label = class_names[class_id]
            confidence = round(float(score), 2)
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f'{label} {confidence}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the frame
    cv2.imshow('Real-Time Object Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()