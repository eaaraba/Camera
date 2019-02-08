# Setup

import numpy as np
import serial
import time
import sys
import cv2


class CV:

    def __init__(self):
        self.arduino = serial.Serial('COM4', 115200)
        time.sleep(0.75)
        print("Connected to Arduino...")
        self.value1 = 0
        self.value2 = 0
        self.LEDIndex = 0
        self.imgIndex = 0
        self.faceHeight = 0
        self.faceWidth = 0
        self.faceInFrame = True
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)



    def LEDonoff(self):
        if self.LEDIndex == 0:
            self.value1 = 49
            self.value2 = 13
            self.arduino.write(bytearray([self.value1, self.value2]))
            self.LEDIndex = 1
            print("LED ON")
        elif self.LEDIndex == 1:
            self.value1 = 48
            self.value2 = 13
            self.LEDIndex = 0
            self.arduino.write(bytearray([self.value1, self.value2]))
            print("LED OFF")

    def coordinates(self):
        roi_color = self.img[self.y:self.y + self.h, self.x:self.x + self.w]
        cv2.rectangle(self.img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 0), 5)
        self.xx = int((self.x + (self.x + self.w)) / 6)
        self.faceWidth = int(self.w)
        self.yy = int((self.y + (self.y + self.h)) / 6)
        self.faceHeight = int(self.h)
        print("x " + str(self.x), "w " + str(self.w), "y " + str(self.y), "h " + str(self.h))
        self.x = int(self.xx)
        self.xcoordinate = 50
        self.y = int(self.yy)
        self.ycoordinate = 51

        center = (self.x, self.y)
        CV.ArduinoSend(self)
        """print("Center of Rectangle is :", center, '\n \n')"""
        if self.faceInFrame == True and self.faceWidth <= 120 and self.faceHeight <= 120:
            self.imgIndex += 1
            self.faceInFrame = False
            cv2.imwrite("Images\LatestImage" + str(self.imgIndex) + ".jpg", self.img)
        time.sleep(0.01)
        cv2.imshow('img', self.img)

    def ArduinoSend(self):
        self.arduino.write(bytearray([self.xcoordinate, self.x]))
        self.arduino.write(bytearray([self.ycoordinate, self.y]))

    def detection(self):
        ret, self.img = self.cap.read()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        for (self.x, self.y, self.w, self.h) in faces:
            CV.coordinates(self)
        cv2.imshow('img', self.img)
        if faces == ():
            self.faceInFrame = True
            print(self.faceInFrame)

    def loop(self):
        while 1:
            images.detection()
            k = cv2.waitKey(30) & 0xff  # 3
            if k == 27:
                break
            elif k == 111:  # if O(letter o not 0) is pressed the LED(pin 13) will be turned on or off depending on it's current state. The pin has to start as being LOW
                images.LEDonoff()


images = CV()

images.loop()