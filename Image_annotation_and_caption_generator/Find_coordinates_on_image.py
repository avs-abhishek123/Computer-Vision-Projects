
# importing the module
import cv2
import matplotlib.pyplot as plt

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        # cv2.imshow('image', img)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([]) # optional line of code, just to hide tick values on X and Y axis if needed
        plt.show()
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        # cv2.imshow('image', img)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([]) # optional line of code, just to hide tick values on X and Y axis if needed
        plt.show()
 
# driver function
if __name__=="__main__":
 
    # reading the image
   
    img = cv2.imread('images/sunset_hand.jpg', 0)
    # img = cv2.imread('/content/drive/MyDrive/Computer_Vision_Projects/images/Wednesday-3.jpg', 0)

    print(img)
    # displaying the image
    # cv2.imshow('image', img)
    plt.imshow(img)
    plt.xticks([]), plt.yticks([]) # optional line of code, just to hide tick values on X and Y axis if needed
    plt.show()
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()