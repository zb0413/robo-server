import unittest
import os
import tempfile
from PIL import Image # For creating dummy image
# Assuming file_utils.py is accessible via PYTHONPATH or relative path adjustments if necessary
# For simplicity in this subtask, we'll assume 'app' is in PYTHONPATH
# Or, more robustly, the test runner would handle this.
# from ..app import file_utils  # This relative import might not work directly with `python -m unittest` from root
# Let's try to make it runnable from the `backend` directory as `python -m unittest discover`
# by temporarily adding app to sys.path or using an approach that works with common test runners.

# For testing purposes, we might need to adjust sys.path if running tests from the 'backend' directory directly.
# A better setup would involve a proper package structure or using pytest which handles paths more gracefully.
import sys
# Add the parent directory of 'app' to sys.path to allow 'from app import ...'
# This assumes the test is run from 'backend/tests' or 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.file_utils import (
    get_file_type,
    get_image_metadata,
    get_text_metadata,
    get_other_metadata
    # We will not test ffmpeg-dependent functions (get_video_metadata, get_audio_metadata) in this basic unit test
    # as they require ffmpeg to be installed and actual media files.
    # Testing them would typically be part of integration testing or require mocking ffmpeg.
)

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_files = {}

        # Create a dummy text file
        self.test_files['text'] = os.path.join(self.test_dir.name, "test.txt")
        with open(self.test_files['text'], "w") as f:
            f.write("This is a test file.")

        # Create a dummy image file (PNG)
        self.test_files['image'] = os.path.join(self.test_dir.name, "test.png")
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save(self.test_files['image'])
        
        # Create a dummy 'other' file
        self.test_files['other'] = os.path.join(self.test_dir.name, "test.zip")
        with open(self.test_files['other'], "w") as f:
            f.write("This is a dummy zip file content.")


    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_get_file_type(self):
        self.assertEqual(get_file_type("file.txt"), "text")
        self.assertEqual(get_file_type("image.jpg"), "image")
        self.assertEqual(get_file_type("image.png"), "image")
        self.assertEqual(get_file_type("video.mp4"), "video")
        self.assertEqual(get_file_type("audio.mp3"), "audio")
        self.assertEqual(get_file_type("archive.zip"), "other")
        self.assertEqual(get_file_type("document.pdf"), "other") # Assuming PDF is 'other' by default
        # Test with one of our created files
        self.assertEqual(get_file_type(self.test_files['text']), "text")
        self.assertEqual(get_file_type(self.test_files['image']), "image")
        self.assertEqual(get_file_type(self.test_files['other']), "other")


    def test_get_text_metadata(self):
        file_path = self.test_files['text']
        metadata = get_text_metadata(file_path)
        self.assertEqual(metadata["name"], "test.txt")
        self.assertEqual(metadata["file_size_bytes"], os.path.getsize(file_path))
        self.assertEqual(metadata["type"], "text")

    def test_get_image_metadata(self):
        # This test is basic for image metadata as location is a placeholder
        # and detailed EXIF parsing is not deeply implemented.
        file_path = self.test_files['image']
        metadata = get_image_metadata(file_path)
        self.assertEqual(metadata["name"], "test.png")
        self.assertEqual(metadata["file_size_bytes"], os.path.getsize(file_path))
        self.assertEqual(metadata["type"], "image")
        # self.assertIsNone(metadata["location"]) # Default is None

    def test_get_other_metadata(self):
        file_path = self.test_files['other']
        metadata = get_other_metadata(file_path)
        self.assertEqual(metadata["name"], "test.zip")
        self.assertEqual(metadata["file_size_bytes"], os.path.getsize(file_path))
        self.assertEqual(metadata["type"], "other")

if __name__ == '__main__':
    unittest.main()
```
