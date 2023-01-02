# SURF (Speeded-Up Robust Features)
# https://medium.com/data-breach/introduction-to-surf-speeded-up-robust-features-c7396d6e7c4e
# sift and surf are patented, so use orb of openCV

#  =========================================================================

# scale-invariant feature transform (SIFT)
# https://www.i2tutorials.com/what-are-sift-and-surf/

#  =========================================================================

# SIFT and SURF are patented so not free for commercial use, while ORB is free.
# SIFT and SURF detect more features then ORB, but ORB is faster.

#  =========================================================================

# import cv2
# import matplotlib.pyplot as plt
# import numpy as np
# # %matplotlib inline

# # Load the image
# image1 = cv2.imread('images/face.png')

# # Convert the training image to RGB
# training_image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

# # Convert the training image to gray scale
# training_gray = cv2.cvtColor(training_image, cv2.COLOR_RGB2GRAY)

# # Create test image by adding Scale Invariance and Rotational Invariance
# test_image = cv2.pyrDown(training_image)
# test_image = cv2.pyrDown(test_image)
# num_rows, num_cols = test_image.shape[:2]

# rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 30, 1)
# test_image = cv2.warpAffine(test_image, rotation_matrix, (num_cols, num_rows))

# test_gray = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)

# # Display traning image and testing image
# fx, plots = plt.subplots(1, 2, figsize=(20,10))

# plots[0].set_title("Training Image")
# plots[0].imshow(training_image)

# plots[1].set_title("Testing Image")
# plots[1].imshow(test_image)
# plt.show()


# # Detect keypoints and Create Descriptor

# surf = cv2.xfeatures2d.SURF_create(800)

# train_keypoints, train_descriptor = surf.detectAndCompute(training_gray, None)
# test_keypoints, test_descriptor = surf.detectAndCompute(test_gray, None)

# keypoints_without_size = np.copy(training_image)
# keypoints_with_size = np.copy(training_image)

# cv2.drawKeypoints(training_image, train_keypoints, keypoints_without_size, color = (0, 255, 0))

# cv2.drawKeypoints(training_image, train_keypoints, keypoints_with_size, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# # Display image with and without keypoints size
# fx, plots = plt.subplots(1, 2, figsize=(20,10))

# plots[0].set_title("Train keypoints With Size")
# plots[0].imshow(keypoints_with_size, cmap='gray')

# plots[1].set_title("Train keypoints Without Size")
# plots[1].imshow(keypoints_without_size, cmap='gray')
# plt.show()

# # Print the number of keypoints detected in the training image
# print("Number of Keypoints Detected In The Training Image: ", len(train_keypoints))

# # Print the number of keypoints detected in the query image
# print("Number of Keypoints Detected In The Query Image: ", len(test_keypoints))


# # Matching Keypoints

# # Create a Brute Force Matcher object.
# bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck = False)

# # Perform the matching between the SURF descriptors of the training image and the test image
# matches = bf.match(train_descriptor, test_descriptor)

# # The matches with shorter distance are the ones we want.
# matches = sorted(matches, key = lambda x : x.distance)

# result = cv2.drawMatches(training_image, train_keypoints, test_gray, test_keypoints, matches, test_gray, flags = 2)

# # Display the best matching points
# plt.rcParams['figure.figsize'] = [14.0, 7.0]
# plt.title('Best Matching Points')
# plt.imshow(result)
# plt.show()

# # Print total number of matching points between the training and query images
# print("\nNumber of Matching Keypoints Between The Training and Query Images: ", len(matches))

# # https://medium.com/data-breach/introduction-to-surf-speeded-up-robust-features-c7396d6e7c4e

import cv2
import numpy as np
img = cv2.imread("images/face.png", cv2.IMREAD_GRAYSCALE)

# sift = cv2.xfeatures2d.SIFT_create()
# surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=1500)

# keypoints_sift, descriptors = sift.detectAndCompute(img, None)
# keypoints_surf, descriptors = surf.detectAndCompute(img, None)
keypoints_orb, descriptors = orb.detectAndCompute(img, None)

img = cv2.drawKeypoints(img, keypoints_orb, None)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

