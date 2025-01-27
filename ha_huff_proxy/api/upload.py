import os
import shutil
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ha_huff_proxy.config import OUTPUT_DIR, BASE_DIR


router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "", "success": "hide"}
    )

@router.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, filename: str = Form(...), file: UploadFile = File(...)):
    try:
        # Create the file path

        file_path = (
            (OUTPUT_DIR / filename) if filename else (OUTPUT_DIR / file.filename)
        )

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "File uploaded successfully!",
                "success": "success"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": f"Error uploading file: {str(e)}",
                "success": "error"
            }
        )
