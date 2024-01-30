'''
Created for CS-370 Lab Week 3
This is the most basic example of how to play a file using the simpleaudio package
'''

import simpleaudio as sa

'''
TODO: Re-write the above as a function that takes in a filename/filepath as an argument
and plays the sound file
'''
def play_sound(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

if __name__ == '__main__':
    filename = '../sounds/toaster.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing