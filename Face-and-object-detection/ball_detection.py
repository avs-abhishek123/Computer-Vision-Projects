import matplotlib.pyplot as plt
import numpy as np
# import pdb
import cv2

"""
https://stackoverflow.com/questions/54346560/detecting-circle-like-shapes-on-binary-images-with-lots-of-noise

Probably using neural network is a good choice, but you still need to understand and train one of them for your task.

You can use thresholding and gaussian blurring, and as a suggestion I can add using normalized cross correlation for template matching. Basically you take a template (an image of the ball, in your case, or even better, a set of images at different sizes, since ball may have varying size based on the position).

Then you iterate on the image and check when the template is matching. Of course this won't work on images with occlusion, but it may help getting some candidates.

More details about the mentioned process in the paper here (https://ieeexplore.ieee.org/document/5375779) or slides here (http://www.cse.psu.edu/~rtc12/CSE486/lecture07.pdf).
"""

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

if __name__ == "__main__":

    ball = plt.imread('ball.jpg')
    ball = rgb2gray(ball)
    findtheballcol = plt.imread('findtheball.jpg')
    findtheball = rgb2gray(findtheballcol)
    matching_img = np.zeros((findtheball.shape[0], findtheball.shape[1]))

    #METHOD 1
    width = ball.shape[1]
    height = ball.shape[0]
    for i in range(ball.shape[0], findtheball.shape[0]-ball.shape[0]):
        for j in range(ball.shape[1], findtheball.shape[1]-ball.shape[1]):


            # here use NCC or something better
            matching_score = np.abs(ball - findtheball[i:i+ball.shape[0], j:j+ball.shape[1]])
            # inverting so that max is what we are looking for
            matching_img[i,j] = 1 / np.sum(matching_score)


    plt.subplot(221)
    plt.imshow(findtheball)
    plt.title('Image')
    plt.subplot(222)
    plt.imshow(matching_img, cmap='jet')
    plt.title('Matching Score')
    plt.subplot(223)
    #pick a threshold
    threshold_val = np.mean(matching_img) * 2; #np.max(matching_img - (np.mean(matching_img)))
    found_at = np.where(matching_img > threshold_val)
    show_match = np.zeros_like(findtheball)
    for l in range(len(found_at[0])):
        yb = round(found_at[0][l]-height/2).astype(int)
        yt = round(found_at[0][l]+height/2).astype(int)
        xl = round(found_at[1][l]-width/2).astype(int)
        xr = round(found_at[1][l]+width/2).astype(int)
        show_match[yb: yt, xl: xr] = 1
    plt.imshow(show_match)
    plt.title('Candidates')
    plt.subplot(224)
    # higher threshold
    threshold_val = np.mean(matching_img) * 3; #np.max(matching_img - (np.mean(matching_img)))
    found_at = np.where(matching_img > threshold_val)
    show_match = np.zeros_like(findtheball)
    for l in range(len(found_at[0])):
        yb = round(found_at[0][l]-height/2).astype(int)
        yt = round(found_at[0][l]+height/2).astype(int)
        xl = round(found_at[1][l]-width/2).astype(int)
        xr = round(found_at[1][l]+width/2).astype(int)
        show_match[yb: yt, xl: xr] = 1
    plt.imshow(show_match)
    plt.title('Best Candidate')
    plt.show()