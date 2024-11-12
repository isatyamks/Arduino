import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the serial line
ser = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino's port

# Set up the plot
fig, ax = plt.subplots()
x_data, y_data = [], []

def update(frame):
    line = ser.readline().decode('utf-8').strip()
    data = line.split(',')
    if len(data) == 7:  # Ensure we have all sensor values
        x_data.append(len(x_data))
        y_data.append([int(val) for val in data])

        ax.clear()
        for i in range(7):
            ax.plot(x_data, [y[i] for y in y_data], label=f'Sensor {i+1}')
        
        ax.legend(loc='upper right')
        ax.set_ylim(-0.5, 1.5)  # Assuming digital sensor output

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
