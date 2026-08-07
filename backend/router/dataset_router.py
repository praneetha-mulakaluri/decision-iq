from fastapi import APIRouter, UploadFile, File
from models.datasetProfileRespone import DatasetProfileResponse
from services.dataset_service import process_csv

router = APIRouter(prefix="/csv", tags=["CSV"])

@router.post("/upload", response_model=DatasetProfileResponse)
async def analyze_dataset(file: UploadFile = File(...)):
    return await process_csv(file)