# import all the required modules

import numpy as np
import serial
import time
import sys
import cv2

# Setup Communication path for arduino on port COM4 and a baudrate of 9600 and setup variables for sending data to the Arduino
arduino = serial.Serial('COM4', 115200)
time.sleep(0.75)
print("Connected to Arduino...")
value1 = 0
value2 = 0
LEDIndex = 0
Timer = 0
imgIndex = 0

# importing the Haarcascade XML data used for face detection; copy the XML file to the same folder as the code
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture the video stream from web cam; a 1 is used as 0 is the PCs built in web cam
cap = cv2.VideoCapture(0)


def make_1200():  # Set the resolution of the camera  #2
    cap.set(3, 1600)
    cap.set(4, 1200)

# Read the captured image, convert it to Gray image and find faces
while 1:
    ret, img = cap.read()
    cv2.resizeWindow('img', 500, 500)  # Might need to be ('img', 500, 500) resolution of web cam is 1600X1200
    # The following creates lines on the center X and Y-Axises
    cv2.line(img, (500, 250), (0, 250), (0, 255, 0), 1)
    cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 1)

    # The following creates a circle in the middle of the image
    cv2.circle(img, (250, 250), 5, (255, 0, 0), -1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # The video feed has to be in gray scale for this facial recognition to work
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)  # Color, scaleFactor, minNeighbors
    # scaleFactor, used by the program to try and resize potential faces to fit the size of the faces that was used to train the model
    # minNeighbors, used to reduce false positives as it will on detect a face if it can draw multiple ROIs around it
    if faces == ():
        Timer = 0
        imgIndex += 0
        print(Timer)
# detect the face and create a roi based on positional data
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)  # Image to draw on, (x, y, x+w, y+h of the face), color(BGR), stroke (thickness of the line)

        # Center coordinates of roi (Rectangle)
        xx = int((x+(x+h))/6)  # The X value increases from left to right

        # Both the X and Y value has to be divided by two twice as the byte array does not accept values above 255

        yy = int((y+(y+w))/6)  # The Y value is lower the higher the face is
        x = int(xx)
        xcoordinate = 50  # ASCII decimal value for 2
        y = int(yy)
        ycoordinate = 51  # ASCII decimal value for 3


        center = (xx, yy)
        arduino.write(bytearray([xcoordinate, x]))  # First write a two to let the arduino know it is receiving an X-coordinate
        arduino.write(bytearray([ycoordinate, y]))  # First write a three to let the arduino know it is receiving a Y-coordinate
        print("Center of Rectangle is :", center, '\n \n')
        Timer += 1
        print(Timer)
        if Timer == 1:
            cv2.imwrite("Images\LatestImage" + str(imgIndex) + ".jpg", img)
        if Timer == 200:
            Timer = 0
        time.sleep(0.01)

# Display the stream, with the ROI
    cv2.imshow('img', img)  # Can be changed to gray instead of the last img to get have a black and white video feed #2


# Hit 'Esc' to terminate execution or O(letter) to turn on/off the BUILTIN_LED
    k = cv2.waitKey(30) & 0xff  # 3
    if k == 27:
        arduino.write(bytearray([xcoordinate, 90]))
        arduino.write(bytearray([ycoordinate, 0]))
        time.sleep(1000)
        break
    elif k == 111:  # if O(letter o not 0) is pressed the LED(pin 13) will be turned on or off depending on it's current state. The pin has to start as being LOW
        if LEDIndex == 0:
            value1 = 49
            value2 = 13
            arduino.write(bytearray([value1, value2]))
            LEDIndex = 1
            print("LED ON")
        elif LEDIndex == 1:
            value1 = 48
            value2 = 13
            arduino.write(bytearray([value1, value2]))
            LEDIndex = 0
            print("LED OFF")


# LITERATURE LIST
# https://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html#gsc.tab=0  #1
# https://www.codingforentrepreneurs.com/search?q=opencv  #2
# https://www.codingforentrepreneurs.com/blog/opencv-python-face-recognition-and-identification  #2
# https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey  #3
