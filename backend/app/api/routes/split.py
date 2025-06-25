from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
from app.core.pdf_utils import split_pdf
import uuid
import shutil

router = APIRouter()

@router.post("/split")
async def split_pdf_endpoint(
    file: UploadFile = File(...),
    ranges: str = Form(...)
):
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    split_ranges = []
    for part in ranges.split(","):
        start, end = part.split("-")
        split_ranges.append((int(start) - 1, int(end) - 1))
    output_files = []
    output_dir = f"/tmp/split_{uuid.uuid4()}"
    os.makedirs(output_dir, exist_ok=True)
    for idx, (start, end) in enumerate(split_ranges):
        output_files.append(os.path.join(output_dir, f"split_{idx+1}.pdf"))
    split_pdf(file_path, split_ranges, output_files)
    os.remove(file_path)
    import zipfile
    zip_path = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for ofile in output_files:
            zipf.write(ofile, os.path.basename(ofile))
    shutil.rmtree(output_dir)
    return FileResponse(zip_path, filename="splits.zip")