#!/usr/bin/env python3

import OPi.GPIO as GPIO
import time
import threading


servo_1_pin = 7
servo_2_pin = 11

SERVO_STEPS = 60
servo_pause = 0.02                   # 20ms => 50Hz
servo_min_pulse = 0.00125
servo_max_pulse = 0.00175

servo_increment = (servo_max_pulse - servo_min_pulse) / SERVO_STEPS

servo_1_target = 0.0015

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
    servo_1_value = servo_1_target

    while True:
        update_servo_1 = False
        if servo_1_value < servo_1_target:
            servo_1_value += servo_increment
            update_servo_1 = True
        elif servo_1_value > servo_1_target:
            servo_1_value -= servo_increment
            update_servo_1 = True

        if update_servo_1:
            GPIO.output(servo_1_pin, 1)
            time.sleep(servo_1_value)
            GPIO.output(servo_1_pin, 0)
            time.sleep(servo_pause)
            GPIO.output(servo_1_pin, 1)
            time.sleep(servo_1_value)
            GPIO.output(servo_1_pin, 0)
            time.sleep(servo_pause)


setup_gpio()
t_servo = threading.Thread(target=process_servo_cmd)
t_servo.start()

try:
    while True:
        servo_1_target = servo_min_pulse
        time.sleep(5)
        servo_1_target = servo_max_pulse
        time.sleep(5)
except:
    GPIO.cleanup()
