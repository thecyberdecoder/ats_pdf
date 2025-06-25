from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
from app.core.pdf_utils import rotate_pdf
import uuid

router = APIRouter()

@router.post("/rotate")
async def rotate_pdf_endpoint(
    file: UploadFile = File(...),
    angle: int = Form(90)
):
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    output_path = f"/tmp/rotated_{uuid.uuid4()}.pdf"
    rotate_pdf(file_path, output_path, angle)
    os.remove(file_path)
    return FileResponse(output_path, filename="rotated.pdf")