import os
import mimetypes
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import ffmpeg # ffmpeg-python
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type.startswith('text/'):
            return 'text'
    # Fallback for common extensions if mime_type is None or not specific enough
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return 'image'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg']:
        return 'audio'
    elif ext in ['.txt', '.md', '.csv', '.json', '.xml', '.html', '.log']:
        return 'text'
    return 'other'

def get_image_metadata(file_path):
    metadata = {
        "name": os.path.basename(file_path),
        "size_bytes": os.path.getsize(file_path),
        "location": None, # Placeholder for GPS data
        "type": "image"
    }
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                # Example: Look for GPSInfo, this requires more detailed parsing
                if tag_name == "GPSInfo":
                    # GPSInfo is a dict itself, would need further parsing
                    # For simplicity, we are not fully parsing GPS here.
                    metadata["location"] = "GPS data present" # Placeholder
    except Exception as e:
        logger.error(f"Error reading image metadata for {file_path}: {e}")
    return metadata

def get_video_metadata(file_path):
    metadata = {
        "name": os.path.basename(file_path),
        "duration_seconds": 0.0,
        "codec": None,
        "bitrate_kbps": None, # Kilobits per second
        "file_size_bytes": os.path.getsize(file_path),
        "type": "video"
    }
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream:
            metadata["duration_seconds"] = float(video_stream.get('duration', 0))
            metadata["codec"] = video_stream.get('codec_name')
            # Bitrate might be in format section or stream section
            if 'bit_rate' in video_stream:
                metadata["bitrate_kbps"] = int(video_stream['bit_rate']) / 1000
            elif 'tags' in video_stream and 'BPS' in video_stream['tags']: # some formats store it in tags
                 metadata["bitrate_kbps"] = int(video_stream['tags']['BPS'])/1000
            elif 'format' in probe and 'bit_rate' in probe['format']:
                 metadata["bitrate_kbps"] = int(probe['format']['bit_rate']) / 1000


    except ffmpeg.Error as e:
        logger.error(f"Error reading video metadata for {file_path} with ffmpeg.probe: {e.stderr.decode('utf8') if e.stderr else e}")
    except Exception as e:
        logger.error(f"Generic error reading video metadata for {file_path}: {e}")
    return metadata

def get_audio_metadata(file_path):
    metadata = {
        "name": os.path.basename(file_path),
        "sample_rate_hz": None,
        "codec": None,
        "file_size_bytes": os.path.getsize(file_path),
        "duration_seconds": 0.0,
        "type": "audio"
    }
    try:
        probe = ffmpeg.probe(file_path)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        if audio_stream:
            metadata["sample_rate_hz"] = int(audio_stream.get('sample_rate', 0))
            metadata["codec"] = audio_stream.get('codec_name')
            metadata["duration_seconds"] = float(audio_stream.get('duration', 0))

    except ffmpeg.Error as e:
        logger.error(f"Error reading audio metadata for {file_path} with ffmpeg.probe: {e.stderr.decode('utf8') if e.stderr else e}")
    except Exception as e:
        logger.error(f"Generic error reading audio metadata for {file_path}: {e}")
    return metadata

def get_text_metadata(file_path):
    return {
        "name": os.path.basename(file_path),
        "file_size_bytes": os.path.getsize(file_path),
        "type": "text"
    }

def get_other_metadata(file_path):
    return {
        "name": os.path.basename(file_path),
        "file_size_bytes": os.path.getsize(file_path),
        "type": "other"
    }

# Example usage (for testing by the worker if needed):
# if __name__ == '__main__':
#     # Create dummy files for testing
#     os.makedirs('test_files', exist_ok=True)
#     with open('test_files/dummy.txt', 'w') as f: f.write('hello')
#     # Note: Image, video, audio files would need to be actual valid files for metadata extraction to work.
#     # For this subtask, we are focusing on writing the code, not on running it with full test files.
#
#     print(f"Text: {get_text_metadata('test_files/dummy.txt')}")
#     print(f"Type for .txt: {get_file_type('test_files/dummy.txt')}")
#     print(f"Type for .jpg: {get_file_type('dummy.jpg')}")
#     print(f"Type for .mp4: {get_file_type('dummy.mp4')}")
#     print(f"Type for .mp3: {get_file_type('dummy.mp3')}")
#     print(f"Type for .zip: {get_file_type('dummy.zip')}")
