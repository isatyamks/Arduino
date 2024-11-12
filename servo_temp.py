import serial
import time
import keyboard

# Setup the serial connection to the Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

def send_command(command):
    arduino.write(command.encode())

try:
    while True:
        if keyboard.is_pressed('w'):
            send_command('w')
            time.sleep(1)  # Control the speed of the servo
        elif keyboard.is_pressed('s'):
            send_command('s')
            time.sleep(0.1)
        elif keyboard.is_pressed('a'):
            send_command('a')
            time.sleep(0.1)
        elif keyboard.is_pressed('d'):
            send_command('d')
            time.sleep(0.1)
        else:
            time.sleep(0.1)  # Idle

except KeyboardInterrupt:
    print("Program stopped by user")
    arduino.close()
