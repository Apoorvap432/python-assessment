from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import os
from app.services.transformer import Transformer

router = APIRouter()

DATA_DIR = "./data/uploads"
OUTPUT_FILE = "./data/output/output.csv"
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

@router.post("/generate")
def generate_report():
    input_path = os.path.join(DATA_DIR, "input.csv")
    reference_path = os.path.join(DATA_DIR, "reference.csv")

    if not os.path.exists(input_path) or not os.path.exists(reference_path):
        raise HTTPException(status_code=400, detail="Both input.csv and reference.csv must be uploaded first.")

    input_df = pd.read_csv(input_path)
    reference_df = pd.read_csv(reference_path)

    transformer = Transformer()
    output_df = transformer.apply_transformations(input_df, reference_df)
    output_df.to_csv(OUTPUT_FILE, index=False)

    return {"message": "Report generated successfully."}

@router.get("/download")
def download_report():
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(status_code=404, detail="Report not found. Generate it first.")
    return FileResponse(OUTPUT_FILE, media_type='text/csv', filename="output.csv")
