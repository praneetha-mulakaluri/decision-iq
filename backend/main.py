from fastapi import FastAPI
from router.dataset_router import router as csv_router

app = FastAPI()

app.include_router(csv_router)