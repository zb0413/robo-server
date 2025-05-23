from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
# Assuming database.py is in the same directory (app)
from .database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True, index=True) # Using String for UUIDs if that's the plan
    name = Column(String, index=True)
    tags = Column(JSON, nullable=True) # Storing list of strings as JSON
    update_time = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, unique=True) # Path to the root directory
    file_counts = Column(JSON, default={}) # e.g., {"images": 10, "videos": 5}
    total_video_duration = Column(Float, default=0.0) # in seconds
    disk_size_bytes = Column(Integer, default=0) # in bytes

    details = relationship("ResourceDetail", back_populates="resource")

class ResourceDetail(Base):
    __tablename__ = "resource_details"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(String) # 'image', 'video', 'audio', 'text', 'other'
    file_path = Column(String, unique=True)
    resource_id = Column(String, ForeignKey("resources.id"))

    resource = relationship("Resource", back_populates="details")

# Pydantic models (in models.py) will be used for API request/response validation
# SQLAlchemy models (here) are for database interaction.
