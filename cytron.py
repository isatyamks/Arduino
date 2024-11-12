import RPi.GPIO as GPIO
import curses
import cv2
import subprocess
import numpy as np
from threading import Thread

# Define motor control functions
def forward(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Set Motor A and Motor B to forward direction
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Forward")

def backward(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Set Motor A and Motor B to backward direction
    GPIO.output(dir_a_pin, GPIO.LOW)
    GPIO.output(dir_b_pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Backward")

def rotate_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A backward, Motor B forward
    GPIO.output(dir_a_pin, GPIO.LOW)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Rotate Left")

def rotate_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A forward, Motor B backward
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    print("Rotate Right")

def turn_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A forward slower, Motor B forward faster
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(25)
    pwm_b.ChangeDutyCycle(75)
    print("Turn Left")

def turn_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A forward faster, Motor B forward slower
    GPIO.output(dir_a_pin, GPIO.HIGH)
    GPIO.output(dir_b_pin, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(75)
    pwm_b.ChangeDutyCycle(25)
    print("Turn Right")

def stop(pwm_a, pwm_b):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Stop")

def cleanup(pwm_a, pwm_b):
    stop(pwm_a, pwm_b)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

# Function to start live camera feed (unchanged)
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
    # Initialize GPIO settings
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dir_a_pin, GPIO.OUT)
    GPIO.setup(pwm_a_pin, GPIO.OUT)
    GPIO.setup(dir_b_pin, GPIO.OUT)
    GPIO.setup(pwm_b_pin, GPIO.OUT)

    # Create PWM objects
    pwm_a = GPIO.PWM(pwm_a_pin, 100)  # Frequency set to 100 Hz
    pwm_b = GPIO.PWM(pwm_b_pin, 100)  # Frequency set to 100 Hz

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
            elif key == curses.KEY_UP:
                forward(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_DOWN:
                backward(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_LEFT:
                turn_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == curses.KEY_RIGHT:
                turn_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == ord('a'):
                rotate_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == ord('d'):
                rotate_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin)
            elif key == ord(' '):
                stop(pwm_a, pwm_b)
    finally:
        cleanup(pwm_a, pwm_b)
        curses.endwin()
        camera_thread.join()

# Define GPIO pins for Cytron MD10C
DIR_A_PIN = 17  # Direction for Motor A
PMWA_PIN = 22   # PWM for Motor A

DIR_B_PIN = 23  # Direction for Motor B
PMWB_PIN = 25   # PWM for Motor B

# Run main function with GPIO pins
curses.wrapper(main, DIR_A_PIN, PMWA_PIN, DIR_B_PIN, PMWB_PIN)