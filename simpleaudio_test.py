import sys
import simpleaudio as sa
from interface import Interface

def play_sound(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

interface = Interface()


if interface.play:
    for filename in interface.play:
        play_sound(filename)

if interface.layer:
    play_objs = [sa.WaveObject.from_wave_file(filename).play() for filename in interface.layer]
    for play_obj in play_objs:
        play_obj.wait_done()

if interface.sequence:
    for filename in interface.sequence:
        play_sound(filename)



