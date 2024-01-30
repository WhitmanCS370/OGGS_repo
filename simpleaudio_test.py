import sys
import simpleaudio as sa

def play_sound(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

if sys.argv[1] == '-p' or sys.argv[1] == '--play' :
    for filename in sys.argv[2:]:
        play_sound(filename)
    sys.exit(0)
