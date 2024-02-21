import os
import unittest
from unittest.mock import patch, MagicMock
from manager import *
from audio import *


class Audio_test(unittest.TestCase):
    """
    Tests for audio playback functionality, including play, layer, and sequence.
    """
    @patch('simpleaudio.WaveObject.from_wave_file')
    def test_play_single_sound(self, mock_wave):
        """
        Test playing a single sound.
        """
        player = Player()
        player.play('sounds/old-sounds/coffee-slurp-2.wav')
        mock_wave.assert_called_once_with('sounds/old-sounds/coffee-slurp-2.wav')

    @patch('simpleaudio.WaveObject.from_wave_file')
    def test_layer_sounds(self, mock_wave):
        """
        Test layering multiple sounds.
        """
        audio_effects = AudioEffects()
        files = ['sounds/old-sounds/coffee-slurp-2.wav', 'sounds/old-sounds/coffee-slurp-3.wav']
        audio_effects.layer(files)
        self.assertEqual(mock_wave.call_count, len(files))

    @patch('simpleaudio.WaveObject.from_wave_file')
    def test_sequence_sounds(self, mock_wave):
        """
        Test sequencing sounds.
        """
        audio_effects = AudioEffects()
        files = ['sounds/old-sounds/coffee-slurp-2.wav', 'sounds/old-sounds/coffee-slurp-3.wav']
        audio_effects.sequence(files)
        self.assertEqual(mock_wave.call_count, len(files))

class FileManager_test(unittest.TestCase):
    """
    test funtctionality of the FileManager
    """
    def setUp(self):
        self.file_manager = FileManager()
        self.test_dir = 'old-sounds'
        self.test_file = 'coffee-slurp-4.wav'
        # Ensure test setup is valid


    def test_rename(self):
        """
        Test renaming functionality within the FileManager.
        """
        original_filename = self.test_file
        new_filename = 'temp_test_rename.wav'
        self.file_manager.rename(self.test_dir, original_filename, new_filename)
        self.assertTrue(os.path.exists(os.path.join('./sounds/', self.test_dir, new_filename)))
        # Cleanup
        self.file_manager.rename(self.test_dir, new_filename, original_filename)


    def test_delete(self):
        """
        Test deleting a file using FileManager.
        """
        pass

    def test_list_files(self):
        """
        Test listing files within a directory.
        """
        files = self.file_manager.list_files(self.test_dir)
        self.assertIn(self.test_file, files, f"{self.test_file} should be listed in {self.test_dir}")


if __name__ == "__main__":
    print("Current Working Directory:", os.getcwd())
    unittest.main()