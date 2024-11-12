from pydub import AudioSegment
from pydub.playback import play
import numpy as np
from scipy.fft import fft
import serial
import time

# Setup for Arduino
ser = serial.Serial('COM5', 9600)  # Adjust COM port and baud rate as needed
file_path = 'whoopty.mp3'
# Load and process the audio file
def process_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1).set_frame_rate(44100)  # Mono, 44.1kHz
    samples = np.array(audio.get_array_of_samples())
    return samples

def get_beat_volume(samples):
    # Apply FFT to detect beats or volume changes
    N = len(samples)
    T = 1.0 / 44100.0
    yf = fft(samples)
    xf = np.fft.fftfreq(N, T)[:N//2]
    
    # Calculate volume as the sum of the absolute values of the FFT
    volume = np.sum(np.abs(yf))
    
    # Detect beats based on peak frequency
    peak_freq = np.argmax(np.abs(yf[:N//2]))
    
    return volume, peak_freq

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Main function
def main():
    audio_file = 'whoopty.mp3'  # Replace with your audio file path
    samples = process_audio(audio_file)
    
    # Analyze beats and volume
    volume, peak_freq = get_beat_volume(samples)
    
    # Map volume and frequency to servo angles
    angle_volume = map_value(volume, 0, np.max(volume), 0, 180)
    angle_freq = map_value(peak_freq, 0, len(samples)//2, 0, 180)
    
    # Send angles to servos
    ser.write(f'S1:{int(angle_volume)}\n'.encode())
    ser.write(f'S2:{int(angle_freq)}\n'.encode())
    
    # Wait and then clean up
    time.sleep(2)
    ser.close()

if __name__ == "__main__":
    main()
