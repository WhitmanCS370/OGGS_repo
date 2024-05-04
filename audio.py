import os
import numpy as np
from pvrecorder import PvRecorder
import wave, struct 
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime

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
        else:
            self.current_playing=filename
            self.length=len(self.current_playing)

    def play(self):
        """
        This method recieves a filepath and plays it, only accepts .wav or .mp3 files
        """
        self.start_time = datetime.now() # get time to calculate the time_elapsed
        try:
            # print(len(self.current_playing))
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
            # self.time_left = self.length - (elapsed.total_seconds() * 1000) # calculate the time left in the current audio clip
            elapsed = (elapsed.total_seconds() * 1000)
            self.current_playing = self.current_playing[elapsed:] # select only the time left in the audio segment
            # play(AudioSegment.empty()) # play an empty audio segment
        
    def resume(self):
        # print(len(self.current_playing))
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
        sound1=AudioSegment.from_wav(files[0])
        for file in files[1:]:
            sound2= AudioSegment.from_wav(file)
            sound1=sound1+sound2
        play(sound1)
        
    def backward(self,filename,db):
        """
        This method will play an audio file backwards
        """
        wave_object=AudioSegment.from_wav(filename)
        reversed= wave_object.reverse()
        hashlist = list(filename)
        hashlist.insert(-4, '_backward') # create the new filename with suffix _backward
        filename=''.join(hashlist)
        reversed.export(filename,format="wav")
        db.add_from_file(filename)
        db.add_tag_to_file("backward", filename)
        return filename
        
    def sequence(self,files):
        """
        This method will play a given list of audio files in sequence
        """
        for file in files:
            self.set_currently_playing_file(file)
            self.play()
            
    def speed_up(self,filename,speed,db):
        """
        creates a new file but speeds it up
        """
        if speed.isnumeric():
            speed=str(int(speed)*1.0)
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
        db.add_from_file(filename)
        db.add_tag_to_file("sped up", filename)
        return filename
        
            
    def trim(self,filename,startTimeStamp,endTimeStamp,db):
        """
        trims the specified file at the sime stamps stated
        """
        sound = AudioSegment.from_wav(filename)
        # duration = sound.duration_seconds
        sound_export = sound[float(startTimeStamp)*1000:float(endTimeStamp)*1000]
        hashlist = list(filename)
        hashlist.insert(-4, '_trim')
        filename=''.join(hashlist)
        sound_export.export(filename,format="wav")
        db.add_from_file(filename)
        db.add_tag_to_file("trimmed", filename)
        return filename

    def apply_distortion(self, filename, db,gain=20):
        """
        apply a distortion effect to the audio file using specified gain factor
        """
        sound = AudioSegment.from_file(filename)
        samples = np.array(sound.get_array_of_samples())
        # amplify the sound by the gain factor
        amplified_samples = samples * gain
        # clip the samples to introduce distortion
        clipped_samples = np.clip(amplified_samples, -32768, 32767)
        # scaling samples back to the original audio range
        max_int16 = np.max(np.abs(clipped_samples))
        if max_int16 > 0:  # no division by zero
            clipped_samples = clipped_samples * (32767 / max_int16)
        # back to int16
        clipped_samples = clipped_samples.astype(np.int16)
        # create new audio from clipped samples
        distorted_sound = sound._spawn(clipped_samples.tobytes())
        # new filename for the distorted version
        hashlist = list(filename)
        hashlist.insert(-4, '_distorted')
        distorted_filename = ''.join(hashlist)
        distorted_sound.export(distorted_filename, format="wav")
        filename, ext = os.path.splitext(os.path.basename(distorted_filename))
        print(filename, ext)
        db.add_from_file(distorted_filename)
        db.add_tag_to_file("distorted", filename)        
        return distorted_filename
    
    def check_length(self,filename):
        sound = AudioSegment.from_wav(filename)
        duration = sound.duration_seconds
        return duration
    
class Recorder(Player):
    
    def check_inputs(self):
        """
        This method checks that there is an availble audio input
        """
        print("check_inputs")
        for index, device in enumerate(PvRecorder.get_available_devices()):
            print(f"[{index}] {device}")

            
    def record(self,outfileName, db):
        """
        starts recording and waits for the user to press ctrl+c or command+c to stop recording

        """
        filepath = os.path.join(os.curdir, "sounds", str(outfileName)+".wav")
        recorder = PvRecorder(device_index=0, frame_length=512) #(32 milliseconds of 16 kHz audio)
        audio = []
        try:
            recorder.start()
            while True:
                frame = recorder.read()
                audio.extend(frame)
        except KeyboardInterrupt:
            recorder.stop()
            print(filepath.split("/")[-1])
            with wave.open(filepath, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
            db.add_from_file(filepath)
        finally:
            recorder.delete()
        return filepath
            
    def get_DateTime(self):
        today=datetime.now()
        return today.strftime("%d-%m-%Y-%H-%M-%S")
        

