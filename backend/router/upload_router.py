from fastapi import APIRouter, UploadFile, File
from services.upload_service import process_csv

router = APIRouter(prefix="/csv", tags=["CSV"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    return await process_csv(file)