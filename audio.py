from os import walk
from pvrecorder import PvRecorder
import wave, struct 
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

class Player:

    def __init__(self): 
        self.current_playing = None # the currently playing audio file
        self.start_time = 0 # time that the audio clip began playing
        self.pause_time = 0 # time that the audio clip was paused
        self.length = 0 # the overall length of the audio clip

    def set_currently_playing_file(self, filename):
        """
        This is a method to set the currently playing file from a filepath
        """
        if filename.endswith(".wav"):
            self.current_playing = AudioSegment.from_wav(filename)
            self.length = len(self.current_playing)
        elif filename.endswith(".mp3"):
            self.current_playing = AudioSegment.from_mp3(filename)
            self.length = len(self.current_playing)

    def play(self):
        """
        play is a function that recieves a file name and path and plays the sound that is at that filepath
        """
        self.start_time = datetime.now() # get time to calculate the time_elapsed
        try:
            print(len(self.current_playing))
            play(self.current_playing)
        except KeyboardInterrupt: # probably better way to do this in interface (reserach custom exeption?)
            self.pause()
        else: 
            self.current_playing = None # once done playing, clear the currently playing


    def pause(self):
        """
        pause a currently playing audio clip
        """
        self.pause_time = datetime.now() # set the time paused
        if self.current_playing:
            elapsed = self.pause_time - self.start_time # calculate the time elapsed in the current audio clip
            self.time_left = self.length - (elapsed.total_seconds() * 1000) # calculate the time left in the current audio clip
            elapsed = (elapsed.total_seconds() * 1000)
            self.current_playing = self.current_playing[elapsed:] # select only the time left in the audio segment
            # play(AudioSegment.empty()) # play an empty audio segment
        

    def resume(self):
        print(len(self.current_playing))
        self.play() # simply play the currently playing audio clip
        
class AudioEffects(Player):
    """
    
    """
    def __init__(self):
        super()
        
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
        print(path[0][-4:])
        if path[0][-4:]!=".wav":
            path[0]=path[0]+self.get_DateTime()+".wav"
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
        

