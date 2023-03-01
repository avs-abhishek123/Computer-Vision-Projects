#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import numpy as np 
import math
import Tkinter
import sys
from PyQt4 import QtGui
from Tkinter import *
from tkFileDialog import askopenfilename
from matplotlib import pyplot as plt


def nothing(x):
    pass

def image():

    print a
    print N
    print p
    #Phase 1 : color staircasing #########################################################################################################

    # Then We Do Bilateral Filtering with k1 = kernal size and N = number of iterations
    # We do Median Filtering
    # Color quantization floor factor = a

    for x in range(0,N):
        bilateral_filtimg = cv2.bilateralFilter(input_image,9,75,75)

    median_filtimg = cv2.medianBlur(bilateral_filtimg,5)

    [rows,cols,c] = median_filtimg.shape
    colorquantimg = median_filtimg
    for i in xrange(0,rows):
        for j in xrange(0,cols):
            xb = median_filtimg.item(i,j,0)
            xg = median_filtimg.item(i,j,1)
            xr = median_filtimg.item(i,j,2)  
            xb = math.floor(xb/a)*a 
            xg = math.floor(xg/a)*a
            xr = math.floor(xr/a)*a
            colorquantimg.itemset((i,j,0),xb)
            colorquantimg.itemset((i,j,1),xg)
            colorquantimg.itemset((i,j,2),xr)

        # Phase2 : Edge Extraction ############################################################################################################

        # Appy Median Filter to the image 
        # Canny Edge Detection
        # Dialation of the detected edges
        # Edgefilter
        #p = cv2.getTrackbarPos('Canny Threshold','Toonified Image')

    median_filtimg2 = cv2.medianBlur(input_image,5)

    edges = cv2.Canny(median_filtimg2,p,2*p)
    dialateimg =  cv2.dilate(edges,np.ones((3,3),'uint8'))
    edges_inv = cv2.bitwise_not(dialateimg)
    ret,thresh = cv2.threshold(edges_inv,127,255,0)
        #cv2.imshow('edges',thresh)
    contours, hierarchy = cv2.findContours(thresh,1,2)
    img_contours = cv2.drawContours(thresh, contours, -1, (0,0,0), 3)
    print img_contours
        #cv2.imshow('counters',img_contours)

        ############################### Recombine both the images ##############################################################################
    global finalimg
    finalimg = colorquantimg
    for i in xrange(0,rows):
        for j in xrange(0,cols):
            if edges_inv.item(i,j) == 0:
                finalimg.itemset((i,j,0),0)
                finalimg.itemset((i,j,1),0)
                finalimg.itemset((i,j,2),0)
    cv2.imshow('Toonified Image',finalimg)       
    cv2.waitKey(0)  

# Main Routine
def filecall():
   # Tk().withdraw()
    filename = askopenfilename()
    global input_image 
    input_image = cv2.imread(filename)

def proceed():
    global a
    global N
    global p
    a = w1.get()
    N = w2.get()
    p = w3.get()
    image()

def quit():
	cv2.destroyWindow('Toonified Image')
	cv2.imshow('Final Output, You can save this one',finalimg)
	cv2.waitKey(0)    
	root.destroy()

root = Tk()
root.geometry("500x500")

l1 = Label(root,text = 'Select Image')
l1.pack()

b1 = Button(root,text = 'Browse',command=filecall)
b1.pack()

b2 = Button(root,text = 'Proceed',command=proceed)
b2.pack()

b3 = Button(root,text = 'Quit',command=quit)
b3.pack()

w1 = Scale(root,label ='Color Quantization Degree(Optimum = 24)',length = 400, from_=10, to=50,orient=HORIZONTAL)  #text=""
w1.pack()

w2 = Scale(root,label = 'Staircase Cartoon Feature Number(Optimum = 5)',length = 400, from_=1, to=10,orient=HORIZONTAL) #text=""
w2.pack()

w3 = Scale(root,label = 'Border Parameter(As per need)', length = 400, from_=10, to=100,orient=HORIZONTAL) #",
w3.pack()

root.mainloop()



    
    

