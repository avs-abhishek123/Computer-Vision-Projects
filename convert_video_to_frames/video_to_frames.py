import cv2
video = cv2.VideoCapture('videos/4k_road_traffic.mp4')

"""
Metadata
Like image data, video data may contain all sorts of additional information or metadata other than the image frames themselves
such as data created, and information about the capture device and other technical information.
If we want a frame from a particular point of a video an important piece of information we can use is the numbers of frames per second, or fps.
To get this information from a video in OpenCV we need to use the variable CAP_PROP_FPS and the function get as follows:
"""

fps = video.get(cv2.CAP_PROP_FPS)
print('frames per second =',fps)
# If you try this out with the attached sample video you should see the video is set to 30.0 fps.

# Finding the frame at a particular time

"""
As we know, video consists of a finite set of discrete image frames.
These are ordered and can be found by the frame number.
If we know the number of frames per second, and the time in the video we want to take a frame from,
we can easily calculate the frame number we want:
"""

minutes = 0
seconds = 28
frame_id = int(fps*(minutes*60 + seconds))
print('frame id =',frame_id)

"""
This tells us that for 0 minutes 28 seconds into the video we need frame 700.
The int() around the calculation makes sure the result we get is an integer value,
since the that’s what we need to find a specific frame.
"""