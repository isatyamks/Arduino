import RPi.GPIO as GPIO
import curses
import subprocess
import numpy as np
import cv2
from threading import Thread

# Motor control functions
def forward(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Forward")

def backward(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    GPIO.output(dir_a_pin, GPIO.LOW)
    GPIO.output(dir_b_pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Backward")

def rotate_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    GPIO.output(dir_a_pin, GPIO.LOW)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Rotate Left")

def rotate_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Rotate Right")

def stop(pwm_a, pwm_b):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Stop")

def cleanup(pwm_a, pwm_b):
    stop(pwm_a, pwm_b)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

# Function to start live camera feed
def start_camera_feed():
    camera_process = subprocess.Popen(
        ['libcamera-vid', '--width', '640', '--height', '480', '-t', '0', '--inline', '--output', '-'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        while True:
            frame_bytes = camera_process.stdout.read(640 * 480 * 3)
            if not frame_bytes:
                break
            frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((480, 640, 3))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error in capturing video: {e}")
    finally:
        camera_process.terminate()
        cv2.destroyAllWindows()

def run_camera():
    camera_thread = Thread(target=start_camera_feed)
    camera_thread.start()
    return camera_thread

def main(stdscr, dir_a_pin, pwm_a_pin, dir_b_pin, pwm_b_pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dir_a_pin, GPIO.OUT)
    GPIO.setup(pwm_a_pin, GPIO.OUT)
    GPIO.setup(dir_b_pin, GPIO.OUT)
    GPIO.setup(pwm_b_pin, GPIO.OUT)

    pwm_a = GPIO.PWM(pwm_a_pin, 100)  
    pwm_b = GPIO.PWM(pwm_b_pin, 100)  

    pwm_a.start(0)
    pwm_b.start(0)

    stdscr.clear()
    stdscr.addstr("Press arrow keys to control the robot. Press 'q' to quit.\n")

    camera_thread = run_camera()

    curses.cbreak()
    stdscr.keypad(True)

    try:
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            stop(pwm_a, pwm_b)  # Stop motors before each command
            if key == curses.KEY_UP:
                forward(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_DOWN:
                backward(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_RIGHT:
                rotate_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_LEFT:
                rotate_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
    finally:
        cleanup(pwm_a, pwm_b)
        curses.endwin()
        camera_thread.join()

# Define GPIO pins for Cytron MD10C
DIR_A_PIN = 17  # Direction for Motor A
PWM_A_PIN = 22  # PWM for Motor A

DIR_B_PIN = 23  # Direction for Motor B
PWM_B_PIN = 25  # PWM for Motor B

# Run main function with GPIO pins
curses.wrapper(main, DIR_A_PIN, PWM_A_PIN, DIR_B_PIN, PWM_B_PIN)