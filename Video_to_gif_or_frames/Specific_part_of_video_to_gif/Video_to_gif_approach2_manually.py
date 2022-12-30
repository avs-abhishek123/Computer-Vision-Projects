"""
You can also save the frames manually by pressing some keys. For instance, you can start saving
frames when key ‘s’ is pressed and stop saving when key ‘q’ is pressed. Once the specific frames
are extracted, we can easily convert them to gifs using imageio as discussed above. Below is the
code for this.
"""

import cv2

import imageio

cap = cv2.VideoCapture('videos/Road_traffic_video_for_object_recognition.mp4')
image_lst = []

prev_key = -1
while True:
    ret, frame = cap.read()
    cv2.imshow('a', frame)
    key = cv2.waitKey(1)
    
    if key == ord('s'):
        key = -1
        prev_key = ord('s')
    
    if key == -1 and prev_key == ord('s'):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_lst.append(frame_rgb)
    
    if key == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

# Convert to gif using the imageio.mimsave method
imageio.mimsave('output/video/specific_fram_2_gif/Road_traffic_video_for_object_recognition2.gif', image_lst, fps=60)