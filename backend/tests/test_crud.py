import unittest
from unittest.mock import patch, MagicMock, call 
import os

# Assuming 'app' is in PYTHONPATH or adjust as necessary.
from app.crud import create_resource_from_directory
from app.models import Resource, ResourceDetail 

# Paths for patching should match where the objects are looked up.
# Functions directly used in crud.py (like os.walk, os.path.isdir, generate_id) are patched in 'app.crud'.
# Functions from file_utils imported into crud.py are patched in 'app.crud' as well.

class TestCrudOperations(unittest.TestCase):

    @patch('app.crud.os.path.isdir')
    @patch('app.crud.os.path.isfile') 
    @patch('app.crud.os.walk')
    @patch('app.crud.get_file_type')
    @patch('app.crud.get_image_metadata')
    @patch('app.crud.get_video_metadata')
    @patch('app.crud.get_text_metadata')
    @patch('app.crud.get_other_metadata') 
    @patch('app.crud.generate_id')
    def test_create_resource_from_directory_with_metadata(self,
                                                         mock_generate_id,
                                                         mock_get_other_metadata,
                                                         mock_get_text_metadata,
                                                         mock_get_video_metadata,
                                                         mock_get_image_metadata,
                                                         mock_get_file_type,
                                                         mock_os_walk,
                                                         mock_os_path_isfile, 
                                                         mock_os_path_isdir):
        # Setup common mocks
        mock_os_path_isdir.return_value = True
        mock_os_path_isfile.return_value = True 
        
        # Mock generate_id to return predictable IDs
        current_id_num = 0
        def id_side_effect_val():
            nonlocal current_id_num
            current_id_num += 1
            return f'test-id-{current_id_num}'
        mock_generate_id.side_effect = id_side_effect_val

        fake_dir_path = '/fake_project'
        mock_files_structure = {
            'image.jpg': 'image',
            'video.mp4': 'video',
            'document.txt': 'text',
            'archive.zip': 'other' 
        }
        mock_file_list = list(mock_files_structure.keys())
        
        mock_os_walk.return_value = [
            (fake_dir_path, [], mock_file_list)
        ]

        # Define side effects for get_file_type
        def file_type_side_effect(file_path_arg): # Renamed to avoid conflict
            filename = os.path.basename(file_path_arg)
            return mock_files_structure.get(filename, 'other')
        mock_get_file_type.side_effect = file_type_side_effect

        # Define return values for metadata functions
        # Ensure these include 'name' and 'file_size_bytes' as crud.py expects them.
        # The 'type' field here is for verification against source, crud.py gets type from get_file_type
        mock_image_meta = {'name': 'image.jpg', 'file_size_bytes': 1024, 'type': 'image', 'width': 100, 'height': 100}
        mock_video_meta = {'name': 'video.mp4', 'file_size_bytes': 2048, 'type': 'video', 'duration_seconds': 60.0, 'codec': 'h264'}
        mock_text_meta = {'name': 'document.txt', 'file_size_bytes': 512, 'type': 'text', 'line_count': 10}
        mock_other_meta = {'name': 'archive.zip', 'file_size_bytes': 4096, 'type': 'other', 'compression_type': 'zip'}


        mock_get_image_metadata.return_value = mock_image_meta
        mock_get_video_metadata.return_value = mock_video_meta
        mock_get_text_metadata.return_value = mock_text_meta
        mock_get_other_metadata.return_value = mock_other_meta
        
        # Call the function
        resource, error = create_resource_from_directory(fake_dir_path)

        # Assertions
        self.assertIsNotNone(resource)
        self.assertIsNone(error)
        # The first ID generated is for the resource itself
        self.assertEqual(resource.id, 'test-id-1')
        self.assertEqual(resource.name, 'fake_project') 
        self.assertEqual(len(resource.details), len(mock_file_list))

        # Check calls to metadata functions
        # Example for one file type, can be expanded
        mock_get_image_metadata.assert_called_with(os.path.join(fake_dir_path, 'image.jpg'))
        mock_get_video_metadata.assert_called_with(os.path.join(fake_dir_path, 'video.mp4'))
        mock_get_text_metadata.assert_called_with(os.path.join(fake_dir_path, 'document.txt'))
        mock_get_other_metadata.assert_called_with(os.path.join(fake_dir_path, 'archive.zip'))
        
        detail_id_counter = 1 # Resource ID is 1, details start from 2
        for detail in resource.details:
            detail_id_counter += 1
            self.assertEqual(detail.id, f'test-id-{detail_id_counter}')
            self.assertIsNotNone(detail.metadata)
            
            # The detail.name is taken from extracted_metadata.get("name", os.path.basename(file_path))
            # So it should match the name in the mocked metadata
            if detail.name == 'image.jpg':
                self.assertEqual(detail.metadata, mock_image_meta)
                self.assertEqual(detail.type, 'image')
            elif detail.name == 'video.mp4':
                self.assertEqual(detail.metadata, mock_video_meta)
                self.assertEqual(detail.type, 'video')
            elif detail.name == 'document.txt':
                self.assertEqual(detail.metadata, mock_text_meta)
                self.assertEqual(detail.type, 'text')
            elif detail.name == 'archive.zip':
                self.assertEqual(detail.metadata, mock_other_meta)
                self.assertEqual(detail.type, 'other')
        
        # Verify file counts and other resource aggregations
        self.assertEqual(resource.file_counts.get('image'), 1)
        self.assertEqual(resource.file_counts.get('video'), 1)
        self.assertEqual(resource.file_counts.get('text'), 1)
        self.assertEqual(resource.file_counts.get('other'), 1)
        self.assertEqual(resource.total_video_duration, mock_video_meta['duration_seconds'])
        expected_total_size = sum(m['file_size_bytes'] for m in [mock_image_meta, mock_video_meta, mock_text_meta, mock_other_meta])
        self.assertEqual(resource.disk_size_bytes, expected_total_size)

if __name__ == '__main__':
    unittest.main()
