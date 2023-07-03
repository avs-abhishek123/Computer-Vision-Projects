# # import cv2
# # import numpy as np

# # # Global variables to store the coordinates of mouse clicks
# # click_x = -1
# # click_y = -1

# # # Mouse callback function
# # def mouse_callback(event, x, y, flags, param):
# #     global click_x, click_y

# #     if event == cv2.EVENT_LBUTTONDOWN:
# #         click_x = x
# #         click_y = y

# # # Create a window and set the mouse callback function
# # cv2.namedWindow('Click Recognizer')
# # cv2.setMouseCallback('Click Recognizer', mouse_callback)

# # # Initialize video capture
# # cap = cv2.VideoCapture(0)

# # while True:
# #     # Read frame from video capture
# #     ret, frame = cap.read()

# #     # Display the frame
# #     cv2.imshow('Click Recognizer', frame)

# #     # Check if a click occurred
# #     if click_x != -1 and click_y != -1:
# #         # Print the coordinates of the click
# #         print(f"Clicked at ({click_x}, {click_y})")
# #         click_x = -1
# #         click_y = -1

# #     # Exit when 'q' is pressed
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # Release resources
# # cap.release()
# # cv2.destroyAllWindows()


# import cv2
# import numpy as np

# # Global variables to store the coordinates of mouse clicks
# click_x = []
# click_y = []
# draw_box = False

# # Mouse callback function
# def mouse_callback(event, x, y, flags, param):
#     global click_x, click_y, draw_box

#     if event == cv2.EVENT_LBUTTONDOWN:
#         click_x.append(x)
#         click_y.append(y)
#         if len(click_x) == 2:
#             draw_box = True

# # Create a window and set the mouse callback function
# cv2.namedWindow('Click Recognizer')
# cv2.setMouseCallback('Click Recognizer', mouse_callback)

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

#         cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

#         # Save the frame and annotation in a text file
#         with open('annotations.txt', 'a') as f:
#             f.write(f"{xmin} {ymin} {xmax} {ymax}\n")

#         # Clear the click coordinates and reset the drawing flag
#         click_x.clear()
#         click_y.clear()
#         draw_box = False

#     # Display the frame
#     cv2.imshow('Click Recognizer', frame)

#     # Exit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()

