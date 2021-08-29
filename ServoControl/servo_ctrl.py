#!/usr/bin/env python3

import OPi.GPIO as GPIO
import time
import threading


servo_1_pin = 7
servo_2_pin = 11

SERVO_STEPS = 10
servo_period = 0.02                   # 20ms => 50Hz
servo_min_pulse = 0.00125
servo_max_pulse = 0.00175
servo_pause = servo_period - servo_max_pulse
servo_increment = (servo_max_pulse - servo_min_pulse) / SERVO_STEPS

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
    while True:
        pulse_1_count = SERVO_STEPS // 2

        if CMD == CMD_LEFT:
            pulse_1_count = 0
        elif CMD == CMD_RIGHT:
            pulse_1_count = SERVO_STEPS

        for i in range(0, SERVO_STEPS):
            state = i < pulse_1_count
            GPIO.output(servo_1_pin, state)
            time.sleep(servo_increment)

        time.sleep(servo_pause)


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