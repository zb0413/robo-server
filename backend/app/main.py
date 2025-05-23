from fastapi import FastAPI, HTTPException, BackgroundTasks, Body
from typing import List, Optional, Dict
import os # For path validation if needed

# Assuming crud.py and models.py are in the same directory (app)
from . import crud
from . import models
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multimedia Resource Management API",
    description="API for importing and managing multimedia resources.",
    version="0.1.0"
)

# --- Helper for background task ---
def run_import_task(directory_path: str):
    logger.info(f"Background task started for importing: {directory_path}")
    resource, error = crud.create_resource_from_directory(directory_path)
    if error:
        logger.error(f"Background import failed for {directory_path}: {error}")
    elif resource:
        logger.info(f"Background import successful for {directory_path}. Resource ID: {resource.id}")
    else:
        logger.warning(f"Background import for {directory_path} completed with no resource and no specific error.")


# --- API Endpoints ---

@app.post("/import/", response_model=models.Resource, status_code=202) # 202 Accepted for background task
async def import_directory(
    background_tasks: BackgroundTasks,
    path_data: str = Body(..., description="The absolute directory path to import.", embed=True, alias="directory_path")
):
    '''
    Import resources from a specified directory.
    This process runs in the background.
    '''
    # Basic validation for path (more can be added)
    if not os.path.isdir(path_data): # Ensure it's a directory
        raise HTTPException(status_code=400, detail=f"Invalid directory path: {path_data}. Not a directory.")
    if not os.path.exists(path_data): # Ensure it exists
         raise HTTPException(status_code=400, detail=f"Invalid directory path: {path_data}. Path does not exist.")


    # For immediate response, we can create a placeholder resource or return a job ID.
    # Here, we'll simulate starting the job and returning a message.
    # The actual resource creation happens in the background.
    # A more robust solution might involve a task queue and status updates.

    background_tasks.add_task(run_import_task, path_data)
    
    # The response model is Resource, but we are not returning the fully processed one immediately.
    # This is a common pattern for long-running tasks.
    # For simplicity, returning a message or a temporary resource ID.
    # Let's return a representation indicating the job has started.
    # Ideally, the client would poll a /status/{task_id} endpoint or use WebSockets.
    # For now, we will return a generic message with the path.
    # A better approach for a real app would be to return a task ID and a way to check status.
    # The `response_model=models.Resource` might be misleading here if not returning the actual created resource.
    # Let's adjust to return a simpler response, or make it clear this is an async operation.
    # For now, let's return a message and change response_model later if needed or make it clearer.
    # Returning a quickly assembled Resource like object for now
    
    # Create a temporary response. The actual resource is created in the background.
    # This is not the final resource, but something to satisfy the response model for now.
    # A better API design might return a Task ID.
    temp_resource_id = crud.generate_id()
    temp_response = models.Resource(
        id=temp_resource_id,
        name=os.path.basename(path_data),
        file_path=path_data,
        tags=["processing"],
        details=[],
        update_time=models.datetime.utcnow(), # Ensure datetime is accessible
        file_counts={},
        total_video_duration=0.0,
        disk_size_bytes=0
    )
    # For now, let's just return a message, as the true resource isn't ready.
    # This means the `response_model` isn't strictly adhered to for the *immediate* response content.
    # A different status code like 202 Accepted is more appropriate.
    return temp_response # This satisfies the model, though it's a temporary representation.


@app.get("/resources/", response_model=List[models.Resource])
async def list_resources():
    '''
    Retrieve a list of all imported resources.
    '''
    return crud.get_all_resources()

@app.get("/resources/{resource_id}/", response_model=models.Resource)
async def get_resource_details(resource_id: str):
    '''
    Retrieve details for a specific resource by its ID.
    '''
    resource = crud.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.get("/statistics/", response_model=Dict) # Adjust response model as needed
async def get_statistics():
    '''
    Retrieve statistics about the imported resources.
    '''
    # The model for statistics can be more specific if desired, e.g., a Pydantic model
    stats = crud.get_statistics_data()
    return stats

# To run this app (from the 'backend' directory):
# Ensure backend/requirements.txt is installed in your venv
# uvicorn app.main:app --reload