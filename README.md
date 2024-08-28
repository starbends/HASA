# HASA
Hyper Accurate Spectrum Analyser

# How it works:

By feeding it a file, of which it is your choice, HASA will determine whether the file can "legally" be called Hi-Fi or Low-Fi. 
It does this in several ways. 

i.     Utilises FFT to convert the signal into a spectrum and also feed back this information in the console.

ii.    Takes the sample rate, and analyses it's true value.

iii.   Considers Noise/Hiss and dynamically removes it based on the amplitude of the track, so that distorted music's values aren't affected, but are still accurate. 

iv.    If the returned value of your file is less than the specified value, it is considered Low-Fi. Currently this value is 19kHz - for leniance with amplitude consistency. However the correct value would be 22.05kHz for flat-line correction. 

# How it can be used: 

i.     Open the executable, and feed it a file (folders coming soon...)

ii.    Wait Patiently... (it's fast) This is meant for quick analysis of downloaded music.

iii.   Once it is complete, it will open a plot window to analyse visually, as well as printing the true value in the console.

# How you can help this project:

i.     Fix the bad code so it's more optimised. I am not a python developer and rop a lot of my code from stackoverflow, forums, etc. 
    -I also have super specific naming schemes for functions and vars from my insane autism but also years working in other languages. 

ii.    help me. please. god help me.

# Things to mention: 

i.     Currently HASA only supports .wav and .flac as Hi-Fi potential files. If you feed it anything else, it'll just skip over it. 

ii.    There's a lot more I want to do with this software, it isn't complete. Please don't consider it a complete piece of work! :)
