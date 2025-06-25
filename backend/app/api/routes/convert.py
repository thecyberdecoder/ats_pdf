from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import uuid
from app.core.pdf_utils import pdf_to_format, format_to_pdf, pdf_to_images

router = APIRouter()

@router.post("/convert")
async def convert_endpoint(
    file: UploadFile = File(...),
    from_type: str = Form(...),
    to_type: str = Form(...)
):
    file_id = str(uuid.uuid4())
    input_path = f"/tmp/{file_id}_{file.filename}"
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)
    output_path = f"/tmp/converted_{uuid.uuid4()}.{to_type.lower()}"

    if from_type == "pdf" and to_type in ["docx", "xlsx", "pptx"]:
        pdf_to_format(input_path, output_path, to_type)
        os.remove(input_path)
        return FileResponse(output_path, filename=f"converted.{to_type}")
    if from_type in ["docx", "xlsx", "pptx"] and to_type == "pdf":
        format_to_pdf(input_path, output_path)
        os.remove(input_path)
        return FileResponse(output_path, filename="converted.pdf")
    if from_type == "pdf" and to_type == "jpg":
        output_folder = f"/tmp/pdf2img_{uuid.uuid4()}"
        os.makedirs(output_folder, exist_ok=True)
        image_paths = pdf_to_images(input_path, output_folder)
        import zipfile
        zip_path = f"{output_folder}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for img in image_paths:
                zipf.write(img, os.path.basename(img))
        os.remove(input_path)
        import shutil
        shutil.rmtree(output_folder)
        return FileResponse(zip_path, filename="images.zip")
    if from_type == "jpg" and to_type == "pdf":
        from PIL import Image
        img = Image.open(input_path)
        img = img.convert('RGB')
        img.save(output_path, "PDF")
        os.remove(input_path)
        return FileResponse(output_path, filename="converted.pdf")
    if from_type == "pdf" and to_type == "pdfa":
        import subprocess
        result = subprocess.run([
            "gs", "-dPDFA", "-dBATCH", "-dNOPAUSE", "-dNOOUTERSAVE", "-sProcessColorModel=DeviceCMYK",
            "-sDEVICE=pdfwrite", "-sPDFACompatibilityPolicy=1",
            f"-sOutputFile={output_path}", input_path
        ], capture_output=True)
        if result.returncode != 0:
            os.remove(input_path)
            return {"error": result.stderr.decode()}
        os.remove(input_path)
        return FileResponse(output_path, filename="converted_pdfa.pdf")
    if from_type == "pdf" and to_type == "html":
        os.remove(input_path)
        return {"error": "PDF to HTML not implemented. Use pdfminer/pdf2htmlEX or a paid API."}
    if from_type == "html" and to_type == "pdf":
        import pdfkit
        pdfkit.from_file(input_path, output_path)
        os.remove(input_path)
        return FileResponse(output_path, filename="converted.pdf")
    os.remove(input_path)
    return {"error": "Conversion not supported."}