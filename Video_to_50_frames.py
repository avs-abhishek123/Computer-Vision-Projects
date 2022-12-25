# to extract every 50th frame
import cv2

# Opens the Video file
cap= cv2.VideoCapture('videos/mom_and_baby_black_and_white.mp4')
i=1
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i%50 == 0:
        cv2.imwrite("output/videos_to_50th_frame/"+'people'+str(i)+'.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()