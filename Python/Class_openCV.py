# Setup

import serial
import time
import cv2
import copy


class Firmware:
    """
    Firmware class to make establishing the gateway between the arduino and the computer
    """
    def __init__(self, port="COM5", baudrate=115200):
        self.port = port            # defining the (usb) port number for the arduino connection
        self.baudrate = baudrate    # defining the baudrate for the arduino connection
        self.arduino = None         # will be used to connect to arduino and sending the data to it

    def connect(self):
        # connecting to the arduino
        self.arduino = serial.Serial(self.port, self.baudrate)  # initiate the connection
        print("Connected to Arduino...")

    def write(self, byte_arr):
        self.arduino.write(byte_arr)


class CV:

    def __init__(self, firmware):
        self.cap = cv2.VideoCapture(1)  # using the cv2.Videocature method to open video capturing device
        self.LEDIndex = 0               # used to show the "state" of the connected LED on the arduino
        self.imgIndex = 0               # int value to help save files into the system, it hold the value to increment it
        self.pic_taken = False          # state value to help the img saving
        self.time_counter = 0


    def loop(self):
        # using a while loop to run the program continuously

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # using the different cascades
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

        while 1:
            self.__reset_timer()
            self.__detection(face_cascade, eye_cascade, smile_cascade)                                          # running the detection private method
            k = cv2.waitKey(1) & 0xff
            if k == 27:                                                 # pressing ESC quitting the program
                self.cap.release()                                      # releasing
                cv2.destroyAllWindows()                                 # destroying the window
                break
            elif k == 111:                                              # if O(letter o not 0) is pressed the LED(pin 13) will be turned on or off depending on it's current state. The pin has to start as being LOW
                self.__led_on_off()

    def __detection(self, face_cascade, eye_cascade, smile_cascade):
        """
        detecting faces, eyes, smiles
        """
        ret, img = self.cap.read()                                        # using the image from the camera
        pure_img = copy.deepcopy(img)                                     # copy the image to be able to save without manipulating
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        for (x, y, w, h) in faces:                                        # using the faces array to extracting the coordinates and use for the eye and smile detection
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
            xx = int((x + (x + w)) / 6)
            yy = int((y + (y + h)) / 6)

            area = (w, h)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray)   # eye detection
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            pos_x = int(xx)
            pos_y = int(yy)

            # smile detection
            smile = smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.16,
                minNeighbors=35,
                minSize=(25, 25),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x2, y2, w2, h2) in smile:
                cv2.rectangle(roi_color, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
                cv2.putText(img, 'Smile', (x, y - 7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)


            # using the firmware to send the center point of detected face
            firmware.write(bytearray([50, pos_x]))
            firmware.write(bytearray([51, pos_y]))

            self.__take_picture(faces, eyes, smile, area, pure_img)

            time.sleep(0.01)

        cv2.imshow('img', img)

    def __reset_timer(self):
        """
        reseting the take picture timer - just use for not to overpopulate the system with bunch of images
        """
        if self.time_counter == 100:
            self.time_counter = 0
            self.pic_taken = False
        self.time_counter += 1

    def __take_picture(self, faces, eyes, smile, area, img):
        """
        taking pictures of several conditions
        - if it detects faces
        - if it detects 2 eyes
        - if it detects the smile
        - and if the face is big enough
        """
        if len(faces) > 0 and len(eyes) > 2 and len(smile) > 0 and self.__face_big_enough(area) and self.pic_taken == False:
            print("take picture")
            self.imgIndex += 1
            self.pic_taken = True
            cv2.imwrite("Images\LatestImage" + str(self.imgIndex) + ".jpg", img)

    def __face_big_enough(self, area):
        """
        check if the face is big enough
        """
        if area[0] > 300 and area[1] > 300:
            return True
        else:
            return False

    def __led_on_off(self):
        """
        using the led on the arduino board - it is not add any functionalty to the code - just fancy
        """
        if self.LEDIndex == 0:  # 0 is off
            firmware.write(bytearray([49, 13]))
            self.LEDIndex = 1
            print("LED ON")
        elif self.LEDIndex == 1:    # 1 is on
            firmware.write(bytearray([48, 13]))
            self.LEDIndex = 0
            print("LED OFF")


firmware = Firmware("COM7", 115200)
images = CV(firmware)
firmware.connect()
images.loop()
