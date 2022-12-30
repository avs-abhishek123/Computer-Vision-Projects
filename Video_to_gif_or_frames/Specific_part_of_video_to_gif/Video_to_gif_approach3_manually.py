"""
This approach is comparatively more tedious. In this, you go over each frame one by one and if
you want to include that frame in gif you press the key ‘a’. To exit, you press the key ‘q’. 
Once the specific frames are extracted, we can easily convert them to gifs using imageio as 
discussed above. Below is the code for this.
"""

import cv2
import imageio

cap = cv2.VideoCapture('videos/Road_traffic_video_for_object_recognition.mp4')
image_lst = []

while True:
    ret, frame = cap.read()
    cv2.imshow('a', frame)
    key = cv2.waitKey(0)

    
    if key == ord('s'):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_lst.append(frame_rgb)
    
    if key == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

# Convert to gif using the imageio.mimsave method
imageio.mimsave('output/video/specific_fram_2_gif/Road_traffic_video_for_object_recognition3.gif', image_lst, fps=60)