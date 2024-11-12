import RPi.GPIO as GPIO
import time

# Define GPIO pins for Motor B
DIR2_PIN = 23   # Direction for Motor B
PWM2_PIN = 25   # PWM for Motor B

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(PWM2_PIN, GPIO.OUT)

# Initialize PWM with a frequency of 100 Hz
pwm_b = GPIO.PWM(PWM2_PIN, 100)
pwm_b.start(0)  # Start with 0% duty cycle

try:
    # Set Motor B to move forward at 50% speed
    GPIO.output(DIR2_PIN, GPIO.HIGH)  # Set direction
    pwm_b.ChangeDutyCycle(50)         # Set speed (50%)

    print("Motor B should be running forward for 5 seconds.")
    time.sleep(5)  # Run the motor for 5 seconds

finally:
    # Stop Motor B and cleanup
    pwm_b.ChangeDutyCycle(0)  # Stop motor
    pwm_b.stop()
    GPIO.cleanup()
    print("Motor B stopped.")





?????????????????????????????




import time

def rotate_left(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A backward, Motor B forward with fine-tuned duty cycle
    GPIO.output(dir_a_pin, GPIO.LOW)  # Motor A backward
    GPIO.output(dir_b_pin, GPIO.HIGH)  # Motor B forward
    pwm_a.ChangeDutyCycle(40)  # Adjust duty cycle if needed
    pwm_b.ChangeDutyCycle(40)
    time.sleep(0.1)  # Optional delay for smoother response
    print("Rotate Left")

def rotate_right(pwm_a, pwm_b, dir_a_pin, dir_b_pin):
    # Motor A forward, Motor B backward with fine-tuned duty cycle
    GPIO.output(dir_a_pin, GPIO.HIGH)  # Motor A forward
    GPIO.output(dir_b_pin, GPIO.LOW)  # Motor B backward
    pwm_a.ChangeDutyCycle(40)  # Adjust duty cycle if needed
    pwm_b.ChangeDutyCycle(40)
    time.sleep(0.1)  # Optional delay for smoother response
    print("Rotate Right")
