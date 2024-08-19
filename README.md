# HASA
Hyper Accurate Spectrum Analyser

# How it works:

By feeding it a folder, of which it is your choice, HASA will determine whether the file can "legally" be called Hi-Fi or Low-Fi. 
It does this in several ways. 

i.     Utilises FFT to convert the signal into a spectrum and also feed back this information in the log.

ii.    Takes the sample rate, and analyses it's true value.

iii.   Considers Noise/Hiss and dynamically removes it based on the amplitude of the track, so that distorted music's values aren't affected, but are still accuarate. 

iv.    If the returned value of your file is less than the specified value, it is considered Low-Fi. Currently this value is 19kHz - for leniance with amplitude consistency. However the correct value would be 22.05kHz for flat-line correction. 

# How it can be used: 

i.     Take your whole folder full of music (or just a selection of folders) and paste the directory into the var "directory_to_analyze"

ii.    Wait Patiently... if it's a big selection of music, it could take several minutes, or potentially hours. It does do each file one at a time. This is meant for quick analysis of downloaded music.

iii.   Once it is complete, it will print a .txt document of all affected files, and which folders they're located within, to the specified location of var "output_file".

# How you can help this project:

i.     Fix the bad code so it's more optimised. I am not a python developer and rop a lot of my code from stackoverflow, forums, etc. 
    -I also have super specific naming schemes for functions and vars from my insane autism but also years working in other languages. 

ii.    help me. please. god help me.

# Things to mention: 

i.     Currently HASA only supports .wav and .flac as Hi-Fi potential files. If you feed it anything else, it'll just skip over it. 

ii.    There's a lot more I want to do with this software, it isn't complete. Please don't consider it a complete piece of work! :)
