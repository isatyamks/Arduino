import serial
import time
import pyautogui

# Setup the serial connection to the Arduino
arduino = serial.Serial('COM4', 9600)  # Replace 'COM4' with your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

def send_command(command):
    arduino.write(command.encode())

try:
    screenWidth, screenHeight = pyautogui.size()  # Get screen size
    sensitivity = 2  # Increase this value to make the movement more sensitive
    
    while True:
        x, y = pyautogui.position()  # Get the current mouse position

        # Apply sensitivity multiplier
        x *= sensitivity
        y *= sensitivity

        print(x,y)

        # Map the mouse position to servo angles, ensuring values stay within 0-180
        servoX = int(min(max((x / screenWidth) * 180, 0), 180))  # X-axis mapped to 0-180
        servoY = int(min(max((y / screenHeight) * 180, 0), 180))  # Y-axis mapped to 0-180

        command = f"{servoX},{servoY}"  # Format the command as "X,Y"
        send_command(command)
        time.sleep(0.05)  # Adjust the delay to control the speed of response

except KeyboardInterrupt:
    print("Program stopped by user")
    arduino.close()
