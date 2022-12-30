import cv2

# Opens the Video file
cap= cv2.VideoCapture('videos/people_walking_grayscale.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite("output/videos2frames/"+'people'+str(i)+'.jpg',frame)
    i+=1

# Releaase the VideoCapture and destroy all windows
cap.release()
cv2.destroyAllWindows()