#fuck you
#bitch
#starbends 2024

import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
import soundfile as sf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import ctypes

def analyze_wav_file(filepath, threshold_khz=19, plot=False):
    try:
        sample_rate, data = wavfile.read(filepath)

        #handles taking the means of the channels in stereo files
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        #fft on audio data
        fft_values = np.abs(fft(data))
        freqs = np.fft.fftfreq(len(fft_values), 1 / sample_rate)

        #considers only the pos freq and ignores the negative half
        positive_freqs = freqs[:len(freqs) // 2]
        positive_fft_values = fft_values[:len(fft_values) // 2]

        #dynamic noise thresholding based on amplitude
        max_amplitude = np.max(positive_fft_values)
        amplitude_threshold = 0.003 * max_amplitude #adjust this value to finetune noise level
        significant_freqs = positive_freqs[positive_fft_values > amplitude_threshold]

        max_freq_khz = np.max(significant_freqs) / 1000 if len(significant_freqs) > 0 else 0

        print(f"File: {filepath}")
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Max Significant Frequency: {max_freq_khz} kHz")

        #returns the answer
        if max_freq_khz >= threshold_khz:
            print("Audio is considered Hi-Fi")
        else:
            print("Audio is considered Low-Fi")

        #this stuff handles the opened plot window
        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(positive_freqs / 1000, positive_fft_values)
            plt.xlabel('Frequency (kHz)')
            plt.ylabel('Normalized Amplitude')
            plt.title(f'Frequency Spectrum of {os.path.basename(filepath)}')
            plt.axvline(x=threshold_khz, color='r', linestyle='--', label='Threshold')
            plt.legend()

            #sets plot window to filename
            plt.get_current_fig_manager().set_window_title(os.path.basename(filepath))
            
            plt.show()  #this blocks until the plot window is closed

        return max_freq_khz >= threshold_khz

    except (IOError, ValueError) as e:
        print(f"Error processing .WAV file {filepath}: {e}")
        return False

def analyze_flac_file(filepath, threshold_khz=19, plot=False):
    try:
        data, sample_rate = sf.read(filepath)

        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        fft_values = np.abs(fft(data))
        freqs = np.fft.fftfreq(len(fft_values), 1 / sample_rate)

        positive_freqs = freqs[:len(freqs) // 2]
        positive_fft_values = fft_values[:len(fft_values) // 2]

        max_amplitude = np.max(positive_fft_values)
        amplitude_threshold = 0.003 * max_amplitude
        significant_freqs = positive_freqs[positive_fft_values > amplitude_threshold]

        max_freq_khz = np.max(significant_freqs) / 1000 if len(significant_freqs) > 0 else 0

        print(f"File: {filepath}")
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Max Significant Frequency: {max_freq_khz} kHz")

        if max_freq_khz >= threshold_khz:
            print("Audio is considered Hi-Fi")
        else:
            print("Audio is considered Low-Fi")

        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(positive_freqs / 1000, positive_fft_values)
            plt.xlabel('Frequency (kHz)')
            plt.ylabel('Normalized Amplitude')
            plt.title(f'Frequency Spectrum of {os.path.basename(filepath)}')
            plt.axvline(x=threshold_khz, color='r', linestyle='--', label='Threshold')
            plt.legend()

            plt.get_current_fig_manager().set_window_title(os.path.basename(filepath))
            
            plt.show()

        return max_freq_khz >= threshold_khz

    except (IOError, ValueError) as e:
        print(f"Error processing .FLAC file {filepath}: {e}")
        return False

def process_audio_file(filepath):
    #check the file has an extension and is supported
    supported_extensions = {'.wav': analyze_wav_file, '.flac': analyze_flac_file}
    _, ext = os.path.splitext(filepath.lower())

    if ext in supported_extensions:
        #call the right function based on the file ext
        supported_extensions[ext](filepath, threshold_khz=19, plot=True) #set plot=True if you want the spectrum plot or False if you don't :)
    else:
        print(f"Unsupported file format: {filepath}")

def select_file():
    root = tk.Tk()
    root.withdraw()  #hides the root tk window

    #opens the file browser window if enter is pressed
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[
            ("Audio Files", "*.wav *.flac"),
            ("All Files", "*.*"),
        ]
    )
    return file_path

def consolename(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def main():
    consolename("HASA - Created by: starbends, 2024")

    while True: #looping this allows multiple inputs. keep that
        print("Drag'n'Drop an audio file into the console.")
        print("alternatively, press Enter to browse for a file manually.")
        
        user_input = input().strip()

        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        if user_input:
            #removes quotes if present
            file_path = user_input.strip('"\'')
            if os.path.isfile(file_path):
                print(f"Selected file: {os.path.basename(file_path)}")
                process_audio_file(file_path)
            else:
                print(f"File not found: {file_path}")
        else:
            #opens file select if no drag'n'drop input
            file_path = select_file()
            if file_path:
                print(f"Selected file: {os.path.basename(file_path)}")
                process_audio_file(file_path)
            else:
                print("No file was selected.")

if __name__ == "__main__":
    main()
