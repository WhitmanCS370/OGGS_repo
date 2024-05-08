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