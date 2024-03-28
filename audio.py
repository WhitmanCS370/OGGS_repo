import simpleaudio as sa
from os import walk
from pvrecorder import PvRecorder
import wave, struct 
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import sql_commands

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
        if filename[-4:]==".wav":
            wave_obj = sa.WaveObject.from_wave_file(filename)
            play_obj = wave_obj.play()
            return play_obj.wait_done()  # Wait until sound has finished playing  
        elif filename[-4:]==".mp3":
            song = AudioSegment.from_mp3(filename)
            print('playing sound using  pydub')
            play(song)
        
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
            
class Recorder(Player):
    
    def check_inputs(self):
        print("check_inputs")
        for index, device in enumerate(PvRecorder.get_available_devices()):
            print(f"[{index}] {device}")
            
    def record(self,path=[".\\sounds\\"]):
        print("Press ctrl + c/command + c to stop recording")
        print(path)
        print(path[-4:])
        
        #for if we can get no argument to work
        #if path[-4:]!=".wav":
        #    path[0]=path[0]+self.get_DateTime()+".wav"
        if path[-4:]!=".wav":
            path=[".\\sounds\\"+path+".wav"]
        else:
            path=[".\\sounds\\"+path]
        print(path)
        recorder = PvRecorder(device_index=0, frame_length=512) #(32 milliseconds of 16 kHz audio)
        audio = []
        try:
            recorder.start()
            while True:
                frame = recorder.read()
                audio.extend(frame)
        except KeyboardInterrupt:
            recorder.stop()
            with wave.open(path[0], 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
        finally:
            recorder.delete()
            
    def get_DateTime(self):
        today=datetime.now()
        return today.strftime("%d-%m-%Y-%H-%M-%S")
        