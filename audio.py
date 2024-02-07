import sys
import simpleaudio as sa

class Player:
    """
    
    """
    def __init__(self):
        print("Player")
        
    def play(self,filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
        
    def isPlaying(self):
        print("is playing")
        
        
class AudioEffects:
    """
    
    """
    def __init__(self):
        print("AudioEffects")
        
    def layer(self):
        print("layer")
        
    def backward(self):
        print("backward")
        
    def sequence(self):
        print("sequence")
        