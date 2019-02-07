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
            self.arduino.write(bytearray([self.value1, self.value2]))
            self.LEDIndex = 0
            print("LED OFF")

    def coordinates(self):
        roi_color = self.img[self.y:self.y + self.h, self.x:self.x + self.w]
        cv2.rectangle(self.img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 0), 5)
        xx = int((self.x + (self.x + self.h)) / 6)

        yy = int((self.y + (self.y + self.w)) / 6)

        x = int(xx)
        self.xcoordinate = 50
        y = int(yy)
        self.ycoordinate = 51

        center = (xx, yy)
        self.arduino.write(bytearray([self.xcoordinate, x]))
        self.arduino.write(bytearray([self.ycoordinate, y]))
        print("Center of Rectangle is :", center, '\n \n')
        cv2.imwrite("Images\LatestImage.jpg", self.img)

    def detection(self):
        ret, self.img = self.cap.read()
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        for (self.x, self.y, self.w, self.h) in faces:
            CV.coordinates(self)
        cv2.imshow('img', self.img)

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