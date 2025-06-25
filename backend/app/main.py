from fastapi import FastAPI
from app.api.routes import merge, split, compress, rotate, convert

app = FastAPI(title="ATS PDF Web Toolkit", version="1.0.0")

app.include_router(merge.router, prefix="/api/pdf")
app.include_router(split.router, prefix="/api/pdf")
app.include_router(compress.router, prefix="/api/pdf")
app.include_router(rotate.router, prefix="/api/pdf")
app.include_router(convert.router, prefix="/api/pdf")