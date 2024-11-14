import RPi.GPIO as GPIO
import time

# Define GPIO pins for Cytron MD10C
DIR1_PIN = 17   # Direction for Motor A
PWM1_PIN = 22   # PWM for Motor A
DIR2_PIN = 23   # Direction for Motor B
PWM2_PIN = 25   # PWM for Motor B

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1_PIN, GPIO.OUT)
GPIO.setup(PWM1_PIN, GPIO.OUT)
GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(PWM2_PIN, GPIO.OUT)

# Initialize PWM with a frequency of 100 Hz

pwm_a = GPIO.PWM(PWM1_PIN, 100)
pwm_b = GPIO.PWM(PWM2_PIN, 100)
pwm_a.start(0)
pwm_b.start(0)

try:
    # Set Motor A to move forward at 50% speed
    GPIO.output(DIR1_PIN, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)  # Adjust speed as needed

    # Set Motor B to move forward at 50% speed
    GPIO.output(DIR2_PIN, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(50)  # Adjust speed as needed

    print("Motors should be running forward for 5 seconds.")
    time.sleep(5)

finally:
    # Stop motors and cleanup
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("Motors stopped.")
