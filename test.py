import RPi.GPIO as GPIO
import keyboard
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define motor control pins
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 23

# Set up motor pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Motor control functions
def motorA_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motorA_reverse():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motorB_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def motorB_reverse():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Keyboard control loop
try:
    print("Use 'W' to move forward, 'S' to move backward, 'A' to turn left, 'D' to turn right, and 'Q' to stop.")
    while True:
        if keyboard.is_pressed('w'):
            motorA_forward()
            motorB_forward()
        elif keyboard.is_pressed('s'):
            motorA_reverse()
            motorB_reverse()
        elif keyboard.is_pressed('a'):
            motorA_reverse()
            motorB_forward()
        elif keyboard.is_pressed('d'):
            motorA_forward()
            motorB_reverse()
        elif keyboard.is_pressed('q'):
            stop_motors()
        else:
            stop_motors()  # Stop the motors if no key is pressed
        time.sleep(0.1)  # Small delay to make the control smoother

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    GPIO.cleanup()
