from fastapi import APIRouter, UploadFile, File
from pdf_compressor import compress_pdf

router = APIRouter()

@router.post("/pdf/compress")
async def compress_pdf_endpoint(file: UploadFile = File(...), quality: int = 75):
    # Save file temporarily
    input_path = f"/tmp/{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())
    output_path = f"/tmp/compressed_{file.filename}"
    compress_pdf(input_path, output_path, quality)
    return FileResponse(output_path, filename=f"compressed_{file.filename}")