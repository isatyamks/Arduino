import RPi.GPIO as GPIO
import time

# Define GPIO pins for Cytron MD10C
DIR_A_PIN = 17  # Direction for Motor A
PMWA_PIN = 22   # PWM for Motor A

DIR_B_PIN = 23  # Direction for Motor B
PMWB_PIN = 25   # PWM for Motor B

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_A_PIN, GPIO.OUT)
GPIO.setup(PMWA_PIN, GPIO.OUT)
GPIO.setup(DIR_B_PIN, GPIO.OUT)
GPIO.setup(PMWB_PIN, GPIO.OUT)

# Create PWM objects
pwm_a = GPIO.PWM(PMWA_PIN, 100)  # Frequency set to 100 Hz
pwm_b = GPIO.PWM(PMWB_PIN, 100)  # Frequency set to 100 Hz

pwm_a.start(0)
pwm_b.start(0)

try:
    # Set both motors to forward
    GPIO.output(DIR_A_PIN, GPIO.HIGH)
    GPIO.output(DIR_B_PIN, GPIO.HIGH)
    
    # Set PWM duty cycle to run motors
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(50)
    
    print("Motors running forward for 5 seconds.")
    time.sleep(5)
    
finally:
    # Stop motors and cleanup
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("Motors stopped.")
