#created by starbends, 2024
#use and modify as you see fit
#credit me if you'd like to - or don't, i don't really care i guess.

import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
import soundfile as sf
import matplotlib.pyplot as plt

def analyze_wav_file(filepath, threshold_khz=19, plot=False):
    try:
        sample_rate, data = wavfile.read(filepath)
        
        #handles taking the means of the channels in stereo files
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        #fft on audio data
        fft_values = np.abs(fft(data))
        freqs = np.fft.fftfreq(len(fft_values), 1/sample_rate)
        
        #considers only the pos freq and ignores the negative half
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft_values = fft_values[:len(fft_values)//2]
        
        #fft value normalisation / dynamic noise adjustment logic
        max_amplitude = np.max(positive_fft_values)
        amplitude_threshold = 0.003 * max_amplitude
        significant_freqs = positive_freqs[positive_fft_values > amplitude_threshold]
        
        if len(significant_freqs) > 0:
            max_freq_khz = np.max(significant_freqs) / 1000
        else:
            max_freq_khz = 0

        #debug shiz for shiz yo
        print(f"File: {filepath}")
        print(f"Sampling Rate: {sample_rate} Hz")
        print(f"Max Significant Frequency: {max_freq_khz} kHz")
        
        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(positive_freqs / 1000, positive_fft_values)
            plt.xlabel('Frequency (kHz)')
            plt.ylabel('Normalized Amplitude')
            plt.title(f'Frequency Spectrum of {os.path.basename(filepath)}')
            plt.axvline(x=threshold_khz, color='r', linestyle='--', label='Threshold')
            plt.legend()
            plt.show()
        
        return max_freq_khz >= threshold_khz

    #don't surf that wave.
    except Exception as e:
        print(f"Error processing WAV file {filepath}: {e}")
        return False

#no dupe comments
def analyze_flac_file(filepath, threshold_khz=19, plot=False):
    try:
        data, sample_rate = sf.read(filepath)
        
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        fft_values = np.abs(fft(data))
        freqs = np.fft.fftfreq(len(fft_values), 1/sample_rate)
        
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft_values = fft_values[:len(fft_values)//2]
        
        max_amplitude = np.max(positive_fft_values)
        amplitude_threshold = 0.003 * max_amplitude
        significant_freqs = positive_freqs[positive_fft_values > amplitude_threshold]
        
        if len(significant_freqs) > 0:
            max_freq_khz = np.max(significant_freqs) / 1000
        else:
            max_freq_khz = 0

        print(f"File: {filepath}")
        print(f"Sampling Rate: {sample_rate} Hz")
        print(f"Max Significant Frequency: {max_freq_khz} kHz")
        
        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(positive_freqs / 1000, positive_fft_values)
            plt.xlabel('Frequency (kHz)')
            plt.ylabel('Normalized Amplitude')
            plt.title(f'Frequency Spectrum of {os.path.basename(filepath)}')
            plt.axvline(x=threshold_khz, color='r', linestyle='--', label='Threshold')
            plt.legend()
            plt.show()

        return max_freq_khz >= threshold_khz
    
    except Exception as e:
        print(f"Error processing FLAC file {filepath}: {e}")
        return False

def analyze_audio_files(directory, threshold_khz=19, output_file="low_fi_folders.txt"):
    low_fi_folders = {}

    for root, _, files in os.walk(directory):
        folder_contains_low_fi = False
        low_fi_files = []

        #filetypes shiz
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if file.endswith('.wav'):
                    is_hi_fi = analyze_wav_file(filepath, threshold_khz)
                elif file.endswith('.flac'):
                    is_hi_fi = analyze_flac_file(filepath, threshold_khz)
                else:
                    print(f"Unsupported file format: {filepath}")
                    continue  #skips unsupported file formats
                
                if is_hi_fi:
                    print(f"{filepath} is Hi-Fi")
                else:
                    folder_contains_low_fi = True
                    low_fi_files.append(file)
                    print(f"{filepath} is Low-Fi")

            #fuck your stupid fucking corrupted files
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

        if folder_contains_low_fi:
            low_fi_folders[root] = low_fi_files
    
    #debug prints
    print(f"Collected Low-Fi folders and files: {low_fi_folders}")
    
    #writing collected data to txt file for your perusing and consideration
    try:
        with open(output_file, 'w') as f:
            if low_fi_folders:
                for folder, files in low_fi_folders.items():
                    f.write(f"Folder: {folder}\n")
                    for file in files:
                        f.write(f"  Low-Fi File: {file}\n")
                    f.write("\n")
                print(f"Low-Fi folders and files have been written to {output_file}")
            else:
                f.write("No Low-Fi folders found.\n")
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")

# Change these to what you'd like to analyze, where you'd like it to output, and threshold adjustment should you want.
directory_to_analyze = r"full_directory_name_here"
output_file = r"output_directory_goes_here"
analyze_audio_files(directory_to_analyze, threshold_khz=19, output_file=output_file)



#this is code to set frequency thresholds to ignore lower frequencies however i'm not utilising it
#min_freq_threshold = 20  # Hz
#significant_freqs = positive_freqs[positive_fft_values > amplitude_threshold]
#significant_freqs = significant_freqs[significant_freqs > min_freq_threshold]
