#!/usr/bin/env python3

import OPi.GPIO as GPIO
import time
import threading


servo_1_pin = 7
servo_2_pin = 11

servo_period = 0.02                   # 20ms => 50Hz
servo_min_pulse = 0.00125
servo_max_pulse = 0.00175
servo_increment = 0.00005
servo_middle = (servo_max_pulse + servo_min_pulse) / 2

CMD = None
CMD_LEFT = "left"
CMD_RIGHT = "right"
CMD_UP = "up"
CMD_DOWN = "down"


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_1_pin, GPIO.OUT)
    GPIO.setup(servo_2_pin, GPIO.OUT)


def process_servo_cmd():
    pulse = servo_middle
    pause = servo_period - servo_middle
    for i in range(0, 10):
        GPIO.output(servo_1_pin, 1)
        time.sleep(pulse)
        GPIO.output(servo_1_pin, 0)
        time.sleep(pause)


setup_gpio()
t_servo = threading.Thread(target=process_servo_cmd)
t_servo.start()

try:
    while True:
        time.sleep(3)

        CMD = CMD_LEFT

        time.sleep(3)

        CMD = CMD_RIGHT

except:
    GPIO.cleanup()