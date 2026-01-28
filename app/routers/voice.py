from fastapi import APIRouter, File, UploadFile
import shutil
import os
# from app.services.voice_handler import VoiceHandler

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to receive audio blob from frontend and transcribe it.
    """
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # In production:
    # text = voice_handler.transcribe_file(temp_filename)
    # os.remove(temp_filename)
    # return {"transcription": text}
    
    return {"transcription": "This is a placeholder for server-side transcription."}
