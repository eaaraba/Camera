# Setup

import serial
import time
import cv2


class Firmware:
    def __init__(self, port="COM5", baudrate=115200):
        self.port = port                                # defining the (usb) port number for the arduino connection
        self.baudrate = baudrate                        # defining the baudrate for the arduino connection
        self.arduino = None                             # will be used to connect to arduino and sending the data to it

    def connect(self):
        # connecting to the arduino
        self.arduino = serial.Serial(self.port, self.baudrate)          # initiate the connection
        print("Connected to Arduino...")

    def write(self, byte_arr):
        self.arduino.write(bytearray(byte_arr))


class CV:
    # initiating the class
    def __init__(self, firmware):
        self.cap = cv2.VideoCapture(0)                                  # using the cv2.Videocature method to open video capturing device
        self.LEDIndex = 0                                               # used to show the "state" of the connected LED on the arduino
        self.imgIndex = 0                                               # int value to help save files into the system, it hold the value to increment it
        self.pic_taken = False                                        # state value to help the img saving
        self.time_counter = 0

    def loop(self):
        # using a while loop to run the program continously
        while 1:
            self.__reset_timer()
            self.__detection()                                          # running the detection private method
            k = cv2.waitKey(1) & 0xff                                   # !!!!!
            if k == 27:                                                 # pressing !!!!!! quitting the program
                self.cap.release()                                      # releasing
                cv2.destroyAllWindows()                                 # destroying the window
                break
            elif k == 111:                                              # if O(letter o not 0) is pressed the LED(pin 13) will be turned on or off depending on it's current state. The pin has to start as being LOW
                self.__led_on_off()

    def __detection(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        for (x, y, w, h) in faces:                                        # that for loop only run if the faces exists
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
            xx = int((x + (x + w)) / 6)
            yy = int((y + (y + h)) / 6)
            center = (x, y)
            area = (w, h)

            pos_x = int(xx)
            pos_y = int(yy)

            firmware.write(bytearray([50, pos_x]))
            firmware.write(bytearray([51, pos_y]))


            # -------- not really need ------------

            # print("Center of Rectangle is :", center)
            # print("Area of the image is :", area)
            # print("\n")
            # -------- not really need ------------

            self.__take_picture(faces, area, img)

            time.sleep(0.04)    # about 24 frame per sec

        cv2.imshow('img', img)

    def __reset_timer(self):
        if self.time_counter == 30:
            self.time_counter = 0
            self.pic_taken = False
        self.time_counter += 1

    def __take_picture(self, faces, area, img):
        if len(faces) > 0 and self.__face_big_enough(area) and self.pic_taken == False:
            print("take picture")
            self.imgIndex += 1
            self.pic_taken = True
            cv2.imwrite("Images\LatestImage" + str(self.imgIndex) + ".jpg", img)

    def __face_big_enough(self, area):
        if area[0] > 300 and area[1] > 300:
            return True
        else:
            return False

    def __led_on_off(self):
        if self.LEDIndex == 0:  # 0 is off
            firmware.write(bytearray([49, 13]))
            self.LEDIndex = 1
            print("LED ON")
        elif self.LEDIndex == 1:    # 1 is on
            firmware.write(bytearray([48, 13]))
            self.LEDIndex = 0
            print("LED OFF")


firmware = Firmware("COM5", 115200)
firmware.connect()
images = CV(firmware)
images.loop()
