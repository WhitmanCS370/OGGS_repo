import simpleaudio as sa
from os import walk

class Player:
    """
    
    """
    def __init__(self): 
        print("Player")
        
    def play(self,filename):
        """
        play is a function that recieves a file name and path and plays the sound that is at that filepath
        """
        print("playing: ", filename)

        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        return play_obj.wait_done()  # Wait until sound has finished playing  
        
    def isPlaying(self):
        if self.play_obj:
            return not self.play_obj.is_playing()
        return True
        
class AudioEffects(Player):
    """
    
    """
    def __init__(self):
        pass
        
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
        
    def sequence(self,files):
        for file in files:
            self.play(file)
            

def play(filename):
        """
        play is a function that recieves a file name and path and plays the sound that is at that filepath
        """
        print("play")
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing 
        
