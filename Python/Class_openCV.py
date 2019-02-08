# Setup

import serial
import time
import cv2


class CV:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None
        self.LEDIndex = 0
        self.imgIndex = 0
        self.faceInFrame = True


    def connect(self):
        self.arduino = serial.Serial(self.port, self.baudrate)
        time.sleep(0.75)
        print("Connected to Arduino...")


    def LEDonoff(self):
        if self.LEDIndex == 0: # 0 is off
            self.arduino.write(bytearray([49, 13]))
            self.LEDIndex = 1
            print("LED ON")
        elif self.LEDIndex == 1: # 1 is on
            self.arduino.write(bytearray([48, 13]))
            self.LEDIndex = 0
            print("LED OFF")

    def coordinates(self):
        cv2.rectangle(self.img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 0), 5)
        self.xx = int((self.x + (self.x + self.w)) / 6)
        self.yy = int((self.y + (self.y + self.h)) / 6)

        self.x = int(self.xx)
        self.y = int(self.yy)
        self.ArduinoSend()

        center = (self.x, self.w, self.y, self.h)
        print("Center of Rectangle is :", center, '\n \n')

        if self.faceInFrame == True:
            self.takepicture()
        time.sleep(0.01)
        cv2.imshow('img', self.img)

    def ArduinoSend(self): # the arduino pin 2 and 3 configured this way to receive only 2 bytes
        self.arduino.write(bytearray([50, self.x]))
        self.arduino.write(bytearray([51, self.y]))

    def takepicture(self):
        self.imgIndex += 1
        self.faceInFrame = False
        cv2.imwrite("Images\LatestImage" + str(self.imgIndex) + ".jpg", self.img)

    def detection(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        ret, self.img = cap.read()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        for (self.x, self.y, self.w, self.h) in faces:
            self.coordinates()
        cv2.imshow('img', self.img)
        if faces == ():
            self.faceInFrame = True
            print(self.faceInFrame)


    def loop(self):
        while 1:
            self.detection()
            k = cv2.waitKey(30) & 0xff  # 3
            if k == 27:
                break
            elif k == 111:  # if O(letter o not 0) is pressed the LED(pin 13) will be turned on or off depending on it's current state. The pin has to start as being LOW
                self.LEDonoff()


images = CV("COM4", 115200)
images.connect()
images.loop()