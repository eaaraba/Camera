/*
   PanTiltDRC
   Arduino code to implement control of pan and tilt  using
        Two RC-servos
        One Arduino
        And a modified version of DRC - The Drogon Remote Control.
   Allow another device talking to us over the serial port to control the
  IO pins.
   DRC originally Copyright (c) 2012 Gordon Henderson
   Full details at:
   http://projects.drogon.net/drogon-remote-control/drc-protocol-arduino/
   Commands:
   @: 0x40 Ping          Send back #: 0x23
   0: 0x30 0xNN  Set servo position of servo on pin 2 to NN (degrees)
   1: 0x31 0xNN  Set servo position of servo on pin 3 to NN (degrees)
*************************************************************************
********
   This file is part of drcAduino:
   Drogon Remote Control for Arduino
   http://projects.drogon.net/drogon-remote-control/
   drcAduino is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   drcAduino is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with drcAduino.  If not, see <http://www.gnu.org/licenses/>.
*************************************************************************
********
*/
// Serial commands
#define CMD_PING        '@'
#define CMD_LED_ON          '1'
#define CMD_LED_OFF         '0'
#define CMD_SERVO_PIN_2       '2'
#define CMD_SERVO_PIN_3       '3'
#define CMD_PIR_PIN_4       '4'
#include <Servo.h>

Servo pan,tilt;  // create servo object to control a servo
// twelve servo objects can be created on most boards



void setup ()
{

  Serial.begin (115200) ;
  Serial.println ("DRC Arduino 1.0") ;
  pan.attach(2);  // attaches the servo on pin 2 to the servo object
  tilt.attach(3);  // attaches the servo on pin 3 to the servo object
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  pinMode(4, INPUT);
  pan.write(90);
  tilt.write(0);
}



int myGetchar ()
{
  int x ;
  while ((x = Serial.read ()) == -1)
    ;
  return x ;
}

void loop ()
{
  unsigned int pin ;
  unsigned int aVal, dVal ;
  int campos ;
  int pos;
  int LEDpin ;
  int Timer;
  int x;
  for (;;)
  {
    if (Serial.available () > 0)
    {
      if (true){
       int y;
       y = digitalRead(4);
       if (y == 0)
         Timer += 1;
       else if (y == 1)
         Timer = 0;
      }
      switch (myGetchar ())
      {
        case CMD_PING:
          Serial.write (CMD_PING) ;
          continue ;


        case CMD_SERVO_PIN_2: //pan
          campos  = myGetchar () ;
          if (campos <= 90){
            pos = pan.read() + 1;
            pan.write(pos);
          }
          else if (campos >= 115){
            pos = pan.read() - 1;
            pan.write(pos);
          }
          continue ;


        case CMD_SERVO_PIN_3: //tilt
          campos  = myGetchar () ;
          if (campos <= 65){
            pos = tilt.read() + 1;
            tilt.write(pos);
          }
          else if (campos >= 85){
            pos = tilt.read() - 1;
            tilt.write(pos);
          }
          delay(50);
          continue ;

        case CMD_LED_OFF:
          LEDpin = myGetchar();
          digitalWrite(LEDpin, LOW);
          delay(50);
          continue ;


       case CMD_LED_ON:
        LEDpin = myGetchar();
        digitalWrite(LEDpin, HIGH);
        delay(50);
        continue;

       case CMD_PIR_PIN_4:
        x = digitalRead(4);
        if (x == 1)
          Serial.println("PIR Sensor is on");
        else if (x == 0 && Timer <= 600)
         Serial.println("The PIR Sensor has been off for less than 30 seconds");
       else if (x == 0 && Timer > 600)
          Serial.println("The PIR Sensor has been off for more than 30 seconds");

      }
    }
  }
}
