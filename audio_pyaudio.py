import pyaudio
import wave
import threading
import time
from pydub import AudioSegment
import tempfile

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
        if self.filepath.endswith('.wav'):
            self.audio = wave.open(self.filepath, 'rb')
        elif self.filepath.endswith('.mp3'):
            print("Converting MP3 to WAV")
            audio = AudioSegment.from_mp3(self.filepath)
            # Convert MP3 to WAV and export to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                audio.export(temp_file.name, format="wav")
                temp_file_path = temp_file.name
            # Open the temporary WAV file with wave.open
            self.audio = wave.open(temp_file_path, 'rb')
        else:
            raise ValueError("Unsupported file format")

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

    def stop(self):
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
        self.reset()

    def reset(self):
        """ Reset stream and file to allow replaying """
        self.audio = wave.open(self.filepath, 'rb')
        self.initialize_stream()
        self.paused = False
        self.stopped = False
        self.current_position = 0  # Reset current position to 0