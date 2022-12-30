"""
Using the fps of the video, we can easily calculate the starting and ending frame number and then
extract all the frames lying between these two. Once the specific frames are extracted, we can
easily convert them to gifs using imageio as discussed above. Below is the code for this where the
frames are extracted from 20 seconds to 25 seconds.
"""
import cv2

import imageio

cap = cv2.VideoCapture('videos/Road_traffic_video_for_object_recognition.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
start_time = 20*fps
end_time = 25*fps
image_lst = []
i = 0

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    if (i>=start_time and i<=end_time):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_lst.append(frame_rgb)

        cv2.imshow('a', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    i +=1

cap.release()
cv2.destroyAllWindows()

# Convert to gif using the imageio.mimsave method
imageio.mimsave('output/video/Road_traffic_video_for_object_recognition1.gif', image_lst, fps=60)