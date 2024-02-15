import sys
import simpleaudio as sa
import os
from os import walk

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
        
class AudioEffects(Player):
    """
    
    """
    def __init__(self):
        print("AudioEffects")
        
    def layer(self,files):
        wavlist=[]
        for file in files:
            if file.endswith('.wav'):
                wavlist.append(sa.WaveObject.from_wave_file(file))
        playlist=[]
        for wave in wavlist:
            playlist.append(wave.play())
        for wave in playlist:
            wave.wait_done()  # Wait until sound has finished playing
            
            
            #self.play(file)
        
    def backward(self):
        print("backward")
        
    def sequence(self):
        print("sequence")
        
