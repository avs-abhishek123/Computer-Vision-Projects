import cv2

# if variance is less than the set threshold
# image is blurred otherwise not
def variance_fn(var):
    if var < 120:
        s = 'Image is Blurred'
    else:
        s = 'Image is not Blurred'
    return s

# Read the image
img = cv2.imread('images/input.jpg')

# Convert to greyscale
grey_1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# make sure that you have saved it in the same folder
# You can change the kernel size as you want
blurImg = cv2.blur(img,(10,10))
grey_2 = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

# Find the laplacian of this image and
# calculate the variance
var_1 = cv2.Laplacian(grey_1, cv2.CV_64F).var()

var_2 = cv2.Laplacian(grey_2, cv2.CV_64F).var()

print("1st image: ",variance_fn(var_1))
print("2nd image: ",variance_fn(var_2), end="")