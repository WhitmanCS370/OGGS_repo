import os
from os import path
import numpy as np
from pvrecorder import PvRecorder
import wave, struct 
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
import threading
import pyaudio
import time
import tkinter as tk
import tempfile

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
            play(self.current_playing)
        except KeyboardInterrupt: # probably better way to do this in interface (reserach custom exeption?)
            self.pause()
        else: 
            self.current_playing = None # once done playing, clear the currently playing

    def sequence(self,files):
        """
        This method will play a given list of audio files in sequence
        """
        for file in files:
            self.set_currently_playing_file(file)
            self.play()

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

class AudioPlayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = None
        self.p = pyaudio.PyAudio()
        self.initialize_stream()
        self.stopped = None
        self.paused = None
        self.current_position = 0  # Initialize current position to 0

    def initialize_stream(self):
        """ Helper method to initialize the PyAudio stream """
        self.audio = wave.open(self.filepath, 'rb')

        self.stream = self.p.open(format=self.p.get_format_from_width(self.audio.getsampwidth()),
                                  channels=self.audio.getnchannels(),
                                  rate=self.audio.getframerate(),
                                  output=True)


    def play(self):
        self.thread = threading.Thread(target=self.stream_audio)
        self.thread.start()

    def stream_audio(self):
        """
        Implementation of streaming. Write data one chunk at a time,
        so it can pause and resume on demand.
        """
        self.audio.setpos(self.current_position)  # Set file position to current position
        while not self.stopped:
            if not self.paused:
                data = self.audio.readframes(1024)
                if not data:
                    break  # End of file
                self.stream.write(data)
            else:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting
        # Update current position when playback stops
        self.current_position = self.audio.tell()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def pausePlay(self):
        # Toggle pause/play state
        if self.paused == True:
            self.paused = False
        elif self.paused == False or not self.paused:
            self.paused = True
        else:
            return None
    def stop(self):
        """Stops the audio(s) that is play"""
        self.stopped = True
        self.thread.join()  # Ensure thread has finished
        self.cleanup()

    def cleanup(self):
        """ Clean up the stream and audio resources """
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.audio.close()
        self.p.terminate()

    def reset(self):
        """ Reset stream and file to allow replaying """
        self.audio = wave.open(self.filepath, 'rb')
        self.initialize_stream()
        self.paused = False
        self.stopped = False
        self.current_position = 0  # Reset current position to 0

    def set_speed(self, speed_factor):
        """Speed up or slow down the audio.
        It creates a new temp file that can be played

        Args:
            speed_factor (float): Factor to adjust the speed (1.0 is normal, 2.0 is double speed, 0.5 is half speed, etc.)
        """

        # Load the entire audio for manipulation
        audio_segment = AudioSegment.from_file(self.filepath)

        # Apply speed change
        new_audio = audio_segment.speedup(playback_speed=speed_factor, chunk_size=150, crossfade=25)

        # Export to a new temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            new_audio.export(temp_file.name, format="wav")
            temp_file_path = temp_file.name

        # Reset the stream with the modified audio
        self.reset()
        self.audio = wave.open(temp_file_path, 'rb')
        self.initialize_stream()

    def skip_to(self, seconds):
        """Skips to a specific position in the audio.

        Args:
            seconds (int): Target position in seconds.
        """

        # Convert skip amount to milliseconds
        seconds = int(seconds)
        frame_position = seconds * self.audio.getframerate()
        if frame_position > self.audio.getnframes():
            frame_position = self.audio.getnframes()  # Prevent seeking past the end

        self.current_position = frame_position
        self.audio.setpos(self.current_position)
        
class AudioEffects:
    """
    This class will be responsible for applying effects to audio files that are being played
    """
    def __init__(self,db):
        super()
        self.db=db
        
    def layer(self,files):
        """
        This method will layer a list of audio files on top of one another
        Generates a new file
        """
        filename = "backwards.wav"
        sound1=AudioSegment.from_wav(files[0])
        for file in files[1:]:
            sound2= AudioSegment.from_wav(file)
            sound1=sound1+sound2
        sound1.export(f"./sounds/{filename}", format="wav")
        self.db.add_from_file(f"./sounds/{filename}")
        return filename
        
    def backward(self,entry):
        """
        This method will play an audio file backwards.
        Generate a new file
        """
        filename=self.db.get_filepath(entry.get())
        wave_object=AudioSegment.from_wav(filename)
        reversed= wave_object.reverse()
        hashlist = list(filename)
        hashlist.insert(-4, '_backward') # create the new filename with suffix _backward
        filename=''.join(hashlist)
        reversed.export(filename,format="wav")
        name, ext = os.path.splitext(os.path.basename(filename))
        self.db.add_from_file(filename)
        self.db.add_tag_to_file("backwards", name)
        return filename
        

            
    def speed_up(self,entry,speed):
        """
        creates a new file but speeds it up
        """
        filename=self.db.get_filepath(entry.get())
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
        self.db.add_from_file(filename)
        self.db.add_tag_to_file("sped up", filename)
        return filename
        
            
    def trim(self,filepath,startTimeStamp,endTimeStamp):
        """
        trims the specified file at the sime stamps stated
        """
        sound = AudioSegment.from_wav(filepath)
        # duration = sound.duration_seconds
        sound_export = sound[float(startTimeStamp)*1000:float(endTimeStamp)*1000]
        hashlist = list(filepath)
        hashlist.insert(-4, '_trim')
        filename=''.join(hashlist)
        sound_export.export(filename,format="wav")
        self.db.add_from_file(filename)
        self.db.add_tag_to_file("trimmed", filename)
        return filename

    def apply_distortion(self, entry,gain=20):
        """
        apply a distortion effect to the audio file using specified gain factor
        """
        filename=self.db.get_filepath(entry.get())
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
        self.db.add_from_file(distorted_filename)
        self.db.add_tag_to_file("distorted", filename)        
        return distorted_filename
    
    def check_length(self,entry):
        filename=self.db.get_filepath(entry.get())
        sound = AudioSegment.from_wav(filename)
        duration = sound.duration_seconds
        return duration
    
class Recorder:
    def __init__(self,db):
        self.isrecording=False
        self.db=db
        self.db.add_all()
            
    def record(self,filename,lbl):
        """
        starts recording and waits for the user to press ctrl+c or command+c to stop recording

        """
        filepath = os.path.join(os.curdir, "sounds", str(filename)+".wav")
        recorder = PvRecorder(device_index=0, frame_length=512) #(32 milliseconds of 16 kHz audio)
        audio = []
        try:
            recorder.start()
            start_time=time.time()
            while self.isrecording:
                frame = recorder.read()
                audio.extend(frame)
                timepassed=time.time()-start_time
                lbl.configure(text=timepassed)
            recorder.stop()
            with wave.open(filepath, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
            self.db.add_from_file(filepath)
            self.db.add_tag_to_file('rec', filename)
            recorder.delete()
        except Exception as e:
            print(f"error occured: {e}")
        
    def click_handler(self,button,path,lbl):
        if self.isrecording:
            self.isrecording=False
            button.config(fg='black')
        else:
            self.isrecording=True
            button.config(fg='red')
            thread=threading.Thread(target=self.record,args=(path,lbl,)).start()
    
class Logic:
    
    def __init__(self,db):
        self.db=db
        
    def get_playlist_list(self):
        playlists=self.db.list_playlists()
        if type(playlists)!=None:
            return list(playlists)+[""]
        else: 
            return []
        
    def get_tag_list(self):
        tags=self.db.list_tags()
        return list(tags)+[""]

    
    def delete_file_with_name(self,name):
        self.db.delete_file_by_name(name)
        
    def add_file(self,file):
        self.db.add_from_file(file)
        
    def rename(self,newFileName,oldFileName):
        self.pathing = path
        self.db.add_from_file(self.pathing.join(self.pathing.curdir, "sounds", newFileName))
        self.db.delete_file_by_name(oldFileName[:-4])
        
    def add_filepath_speed_up(self,entry,amount_entry,audio):
        self.db.add_from_file(audio.speed_up(entry,amount_entry.get()))
    
    def song_playlist(self,playlist_dropdown,entry):
        self.db.song_to_playlist(playlist_dropdown.get(),entry)
    
    def song_tag(self,tag_dropdown,entry):
        self.db.add_tag_to_file(tag_dropdown.get(),entry)
        
    def create_playlist(self,playlist_entry):
        self.db.add_playlist(playlist_entry)
        
    def create_tag(self,tag_entry):
        self.db.add_tag(tag_entry)
        
    def add_filepath_trim(self,entry,hLeft,hRight,audio):
        filepath=self.db.get_filepath(entry.get())
        self.db.add_from_file(audio.trim(filepath,int(hLeft.get()),int(hRight.get())))
    
    def add_filepath(self,file):
        self.db.add_from_file(file)
        
    def input_files(self,treeview):
        try:
            for item in treeview.get_children():
                treeview.delete(item)
            files=self.db.list_files()
            for i in range(len(files)):
                filepath=self.db.get_filepath(files[i])
                treeview.insert("",tk.END,text=f"Item #{i+1}",values=(files[i],filepath,self.db.tags_from_file(files[i]),self.db.get_duration(filepath)))
        except:
            print("didnt work")
            
    def get_files(self):
        return self.db.list_files()
    
    def show_playlist(self,playlist_dropdown,treeview):
        if (playlist_dropdown.get() == ""):
            self.input_files(treeview)
            return
        for item in treeview.get_children():
            treeview.delete(item)
        files=self.db.get_playlist(playlist_dropdown.get())
        for i in range(len(files)):
            title = files[i].split("/")[-1].split(".")[0]
            treeview.insert("",tk.END,text=f"Item #{i+1}",values=(title,files[i],self.db.tags_from_file(title),self.db.get_duration(files[i])))
    
    def show_tag(self,tag_dropdown,treeview):
        if (tag_dropdown.get() == ""):
            self.input_files(treeview)
            return
        for item in treeview.get_children():
            treeview.delete(item)
        files=self.db.get_from_tag(tag_dropdown.get())
        for i in range(len(files)):
            title = files[i].split("/")[-1].split(".")[0]
            treeview.insert("",tk.END,text=f"Item #{i+1}",values=(title,files[i],self.db.tags_from_file(title),self.db.get_duration(files[i])))