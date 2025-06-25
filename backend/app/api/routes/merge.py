from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import os
from app.core.pdf_utils import merge_pdfs
import uuid

router = APIRouter()

@router.post("/merge")
async def merge_pdf(files: list[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = f"/tmp/{file_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(file_path)
    output_path = f"/tmp/merged_{uuid.uuid4()}.pdf"
    merge_pdfs(file_paths, output_path)
    for f in file_paths:
        os.remove(f)
    return FileResponse(output_path, filename="merged.pdf")