#!/usr/bin/env python3

import OPi.GPIO as GPIO
import time


servo_1_pin = 7
servo_2_pin = 11

servo_period = 0.02                   # 20ms => 50Hz
servo_min_pulse = 0.00125
servo_max_pulse = 0.00175
servo_increment = 0.00005
servo_middle = (servo_max_pulse + servo_min_pulse) / 2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_1_pin, GPIO.OUT)
GPIO.setup(servo_2_pin, GPIO.OUT)

CMD = None
CMD_LEFT = "left"
CMD_RIGHT = "right"
CMD_UP = "up"
CMD_DOWN = "down"


def process_servo_cmd():
    pulse = servo_middle
    pause = servo_period - servo_middle
    for i in range(0, 10):
        GPIO.output(servo_1_pin, 1)
        time.sleep(pulse)
        GPIO.output(servo_1_pin, 0)
        time.sleep(pause)


try:
    while True:
        time.sleep(3)

        CMD = CMD_LEFT

        process_servo_cmd()

        time.sleep(3)

        CMD = CMD_RIGHT

        process_servo_cmd()

except:
    GPIO.cleanup()