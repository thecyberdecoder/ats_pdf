from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
from app.core.pdf_utils import compress_pdf
import uuid

router = APIRouter()

@router.post("/compress")
async def compress_pdf_endpoint(
    file: UploadFile = File(...),
    quality: int = Form(60)
):
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    output_path = f"/tmp/compressed_{uuid.uuid4()}.pdf"
    compress_pdf(file_path, output_path, quality)
    os.remove(file_path)
    return FileResponse(output_path, filename="compressed.pdf")