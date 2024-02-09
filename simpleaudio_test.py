import sys
import simpleaudio as sa
from interface import Interface

def play_sound(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

interface = Interface()

for filename in interface.play:
    play_sound(filename)


