from os import walk
from pvrecorder import PvRecorder
import wave, struct 
from pydub import AudioSegment
from pydub.playback import play
import sql_commands
import datetime

class Player:
    """
    This is a class responsible for playing media
    """
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
        This method recieves a filepath and plays it, only accepts .wav or .mp3 files
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
    This class will be responsible for applying effects to audio files that are being played
    """
    def __init__(self):
        super()
        
    def layer(self,files):
        """
        This method will layer a list of audio files on top of one another
        """
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
        
    def backward(self,filename):
        """
        This method will play an audio file backwards
        """
        filename=".\\sounds\\"+filename
        wave_object=AudioSegment.from_wav(filename)
        reversed= wave_object.reverse()
        hashlist = list(filename)
        hashlist.insert(-4, '_backward')
        filename=''.join(hashlist)
        reversed.export(filename,format="wav")
        
    def sequence(self,files):
        """
        This method will play a given list of audio files in sequence
        """
        for file in files:
            self.play(file)
            
    def speed_up(self,filename,speed):
        """
        creates a new file but speeds it up
        """
        if speed.isnumeric():
            speed=str(int(speed)*1.0)
        filename=".\\sounds\\"+filename
        sound = AudioSegment.from_wav(filename)
        so = sound.speedup(float(speed), 150, 25)
        if filename.endswith("_speed",-13,-7) and filename[-7].isnumeric():
            num=float(filename[-7:-4])+float(speed)
            filename=filename[:-7]+str(num)+".wav"
        else:
            hashlist = list(filename)
            hashlist.insert(-4, '_speed'+speed)
            filename=''.join(hashlist)
        so.export(filename,format="wav")
        
            
    def trim(self,filename,startTimeStamp,endTimeStamp):
        """
        trims the specified file at the sime stamps stated
        """
        filename=".\\sounds\\"+filename
        sound = AudioSegment.from_wav(filename)
        duration = sound.duration_seconds
        sound_export = sound[float(startTimeStamp)*1000:float(endTimeStamp)*1000]
        hashlist = list(filename)
        hashlist.insert(-4, '_trim')
        filename=''.join(hashlist)
        sound_export.export(filename,format="wav")
        
    def check_length(self,filename):
        filename=".\\sounds\\"+filename
        sound = AudioSegment.from_wav(filename)
        duration = sound.duration_seconds
        print(duration)

class Recorder(Player):
    
    def check_inputs(self):
        """
        This method checks that there is an availble audio input
        """
        print("check_inputs")
        for index, device in enumerate(PvRecorder.get_available_devices()):
            print(f"[{index}] {device}")

            
    def record(self,path):
        """
        starts recording and waits for the user to press ctrl+c or command+c to stop recording

        """
        print("Press ctrl+c / command+c to stop recording")        
        if path[-4:]!=".wav":
            path=[".\\sounds\\"+path+".wav"]
        else:
            path=[".\\sounds\\"+path]
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
        

