from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from typing import List, Tuple
import fitz  # PyMuPDF
import os
import subprocess

def merge_pdfs(input_paths: List[str], output_path: str):
    merger = PdfMerger()
    for pdf in input_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def split_pdf(input_path: str, ranges: List[Tuple[int, int]], output_paths: List[str]):
    reader = PdfReader(input_path)
    for (start, end), output_path in zip(ranges, output_paths):
        writer = PdfWriter()
        for page_num in range(start, end + 1):
            writer.add_page(reader.pages[page_num])
        with open(output_path, "wb") as out:
            writer.write(out)

def compress_pdf(input_path: str, output_path: str, quality: int = 60):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, compress=quality)
    doc.close()

def rotate_pdf(input_path: str, output_path: str, angle: int):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)
    with open(output_path, "wb") as out:
        writer.write(out)

def pdf_to_format(pdf_path: str, output_path: str, target_format: str):
    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", target_format, pdf_path, "--outdir", os.path.dirname(output_path)
    ], capture_output=True)
    if result.returncode != 0:
        raise Exception(result.stderr)
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    converted_file = os.path.join(os.path.dirname(output_path), f"{basename}.{target_format}")
    os.rename(converted_file, output_path)

def format_to_pdf(input_path: str, output_path: str):
    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", os.path.dirname(output_path)
    ], capture_output=True)
    if result.returncode != 0:
        raise Exception(result.stderr)
    basename = os.path.splitext(os.path.basename(input_path))[0]
    converted_file = os.path.join(os.path.dirname(output_path), f"{basename}.pdf")
    os.rename(converted_file, output_path)

def pdf_to_images(pdf_path: str, output_folder: str):
    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        pix = doc.load_page(page_num).get_pixmap()
        img_path = os.path.join(output_folder, f"page_{page_num+1}.jpg")
        pix.save(img_path)
        image_paths.append(img_path)
    doc.close()
    return image_paths