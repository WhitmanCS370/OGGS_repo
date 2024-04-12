import simpleaudio as sa
from os import walk
from pvrecorder import PvRecorder
import wave, struct 
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
        
    def backward(self,filename):
        filename=".\\sounds\\"+filename
        wave_object=sa.WaveObject.from_wave_file(filename)
        reversed= wave_object.reverse()
        hashlist = list(filename)
        hashlist.insert(-4, '_backward')
        filename=''.join(hashlist)
        reversed.export(filename,format="wav")
        
        
    def sequence(self,files):
        """
        plays 
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
        checks the amount of microphone inputs available and prints them out one by one
        """
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
        