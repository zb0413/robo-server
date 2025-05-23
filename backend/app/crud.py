import os
import uuid
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Assuming models.py and file_utils.py are in the same directory (app)
from .models import Resource, ResourceCreate, ResourceDetail, ResourceDetailCreate
from .file_utils import (
    get_file_type,
    get_image_metadata,
    get_video_metadata,
    get_audio_metadata,
    get_text_metadata,
    get_other_metadata
)
import logging

logger = logging.getLogger(__name__)

# In-memory storage (for now)
# A production app would use a database
db_resources: Dict[str, Resource] = {}
db_resource_details: Dict[str, List[ResourceDetail]] = {} # Maps resource_id to its details

def generate_id() -> str:
    return str(uuid.uuid4())

def create_resource_from_directory(directory_path: str) -> Tuple[Optional[Resource], Optional[str]]:
    if not os.path.isdir(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        return None, "Directory not found"

    resource_id = generate_id()
    resource_name = os.path.basename(directory_path)
    if not resource_name: # Handle case like "path/to/dir/"
        resource_name = os.path.basename(os.path.dirname(directory_path))


    resource_data = ResourceCreate(
        name=resource_name,
        file_path=directory_path,
        update_time=datetime.utcnow(),
        tags=[], # Placeholder for now
        file_counts={},
        total_video_duration=0.0,
        disk_size_bytes=0
    )

    current_resource_details: List[ResourceDetail] = []
    total_disk_size_bytes = 0
    file_counts: Dict[str, int] = {"image": 0, "video": 0, "audio": 0, "text": 0, "other": 0}

    try:
        for root, _, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if not os.path.isfile(file_path): # Skip if it's a symlink to a dir or broken symlink
                    continue

                file_type = get_file_type(file_path)
                metadata = None
                detail_id = generate_id()

                if file_type == 'image':
                    metadata = get_image_metadata(file_path)
                    file_counts['image'] += 1
                elif file_type == 'video':
                    metadata = get_video_metadata(file_path)
                    resource_data.total_video_duration += metadata.get("duration_seconds", 0.0)
                    file_counts['video'] += 1
                elif file_type == 'audio':
                    metadata = get_audio_metadata(file_path)
                    # Add total_audio_duration to Resource model if needed
                    file_counts['audio'] += 1
                elif file_type == 'text':
                    metadata = get_text_metadata(file_path)
                    file_counts['text'] += 1
                else: # 'other'
                    metadata = get_other_metadata(file_path)
                    file_counts['other'] += 1
                
                if metadata:
                    common_detail_data = {
                        "id": detail_id,
                        "name": metadata["name"],
                        "type": file_type,
                        "file_path": file_path,
                    }
                    # Ensure all required fields for ResourceDetailCreate are present if it were used.
                    # Here, we directly construct ResourceDetail which includes 'id'.
                    res_detail = ResourceDetail(**common_detail_data)
                    current_resource_details.append(res_detail)
                    total_disk_size_bytes += metadata.get("file_size_bytes", 0)
                else:
                    logger.warning(f"Could not extract metadata for file: {file_path}")


        resource_data.disk_size_bytes = total_disk_size_bytes
        resource_data.file_counts = file_counts

        # Persist to "DB"
        # Use .model_dump() for Pydantic v2+
        final_resource = Resource(id=resource_id, **resource_data.model_dump(), details=[])
        db_resources[resource_id] = final_resource
        # Storing details separately for in-memory version, actual Resource model has 'details' field
        db_resource_details[resource_id] = current_resource_details

        # For the Resource object returned, embed the details as per the model
        final_resource.details = current_resource_details

        logger.info(f"Successfully processed directory: {directory_path}. Resource ID: {resource_id}")
        return final_resource, None

    except Exception as e:
        logger.error(f"Failed to process directory {directory_path}: {e}", exc_info=True)
        return None, str(e)

def get_resource(resource_id: str) -> Optional[Resource]:
    resource_data = db_resources.get(resource_id)
    if resource_data:
        # Create a new Resource instance or a copy to safely attach details
        # This ensures that the object from db_resources isn't modified if details are later changed on the returned object.
        resource_copy = resource_data.model_copy(deep=True) # Pydantic v2+
        resource_copy.details = db_resource_details.get(resource_id, [])
        return resource_copy
    return None

def get_all_resources() -> List[Resource]:
    all_resources = []
    for res_id, res_data in db_resources.items():
        # Create a copy to avoid modifying the stored object if details are changed later
        res_copy = res_data.model_copy(deep=True) # Pydantic v2+
        res_copy.details = db_resource_details.get(res_id, [])
        all_resources.append(res_copy)
    return all_resources

# Placeholder for statistics - will be expanded in the API endpoint logic
def get_statistics_data() -> Dict:
    total_files = 0
    total_video_duration_seconds = 0.0
    total_audio_duration_seconds = 0.0 # Initialize total audio duration
    type_counts = {"image": 0, "video": 0, "audio": 0, "text": 0, "other": 0}

    for resource_id in db_resources:
        resource = get_resource(resource_id) # Use get_resource to ensure details are loaded
        if resource:
            for type_name, count in resource.file_counts.items():
                type_counts[type_name] = type_counts.get(type_name, 0) + count
                total_files += count
            total_video_duration_seconds += resource.total_video_duration or 0.0
            
            # Sum audio duration from details
            for detail in resource.details:
                if detail.type == 'audio':
                    # This assumes audio_metadata stored duration_seconds in a way that get_resource can retrieve it.
                    # The current get_audio_metadata function returns a dict, not an object with attributes.
                    # This part needs alignment with how audio metadata (esp. duration) is stored and accessed.
                    # For now, let's assume a placeholder or that details would be enriched with this.
                    # If audio_metadata was directly attached to ResourceDetail or accessible:
                    # e.g. if detail contained a field like detail.metadata_attributes['duration_seconds']
                    # We will need to adjust this once file_utils and models are fully integrated.
                    # For now, this part of audio duration sum might not work as intended without further adjustments.
                    # Let's assume a placeholder way to get audio duration from details if available.
                    # This detail might need to be added to ResourceDetail model or handled during its creation.
                    # Example: if get_audio_metadata result was part of ResourceDetail
                    # audio_meta = get_audio_metadata(detail.file_path) # Re-fetching, not ideal
                    # total_audio_duration_seconds += audio_meta.get("duration_seconds", 0.0)
                    pass # Placeholder for summing audio duration correctly


    return {
        "total_files": total_files,
        "type_counts": type_counts,
        "total_video_duration_seconds": total_video_duration_seconds,
        "total_audio_duration_seconds": total_audio_duration_seconds, # Placeholder
        "changes_last_7_days": "Data for 7-day changes not available with in-memory storage."
    }
