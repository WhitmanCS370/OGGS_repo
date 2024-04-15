import pyaudio
import wave
import threading
import time

class AudioPlayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.wf = wave.open(self.filepath, 'rb')
        self.p = pyaudio.PyAudio()
        self.initialize_stream()
        self.stopped = None
        self.paused = None

    def initialize_stream(self):
        """ Helper method to initialize the PyAudio stream """
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)

    def play(self):
        self.thread = threading.Thread(target=self.stream_audio)
        self.thread.start()

    def stream_audio(self):
        """
        Implementation of streaming. Write data one chunk at a time,
        so it can pause and resume on demand.
        """
        while not self.stopped:
            if not self.paused:
                data = self.wf.readframes(1024)
                if not data:
                    break  # End of file
                self.stream.write(data)
            else:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting

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
        self.wf.close()
        self.p.terminate()
        self.reset()

    def reset(self):
        """ Reset stream and file to allow replaying """
        self.wf = wave.open(self.filepath, 'rb')
        self.initialize_stream()
        self.paused = False
        self.stopped = False
