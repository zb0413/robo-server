from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResourceDetailBase(BaseModel):
    name: str
    type: str  # 'image', 'video', 'audio', 'text', 'other'
    file_path: str
    metadata: Optional[Dict[str, Any]] = None

class ResourceDetailCreate(ResourceDetailBase):
    pass

class ResourceDetail(ResourceDetailBase):
    id: str  # Or int, depending on how we generate it

    class Config:
        orm_mode = True # Changed from from_attributes = True for wider Pydantic compatibility

class ResourceBase(BaseModel):
    name: str
    tags: Optional[List[str]] = []
    update_time: datetime = Field(default_factory=datetime.utcnow)
    file_path: str # Path to the root directory of the resource
    file_counts: Dict[str, int] = {} # e.g., {"images": 10, "videos": 5}
    total_video_duration: Optional[float] = 0.0 # in seconds
    disk_size_bytes: Optional[int] = 0 # in bytes

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: str # Or int
    details: List[ResourceDetail] = []

    class Config:
        orm_mode = True # Changed from from_attributes = True

# Example of how IDs might be generated (not part of this subtask, just for context)
# import uuid
# def generate_id():
#     return str(uuid.uuid4())
