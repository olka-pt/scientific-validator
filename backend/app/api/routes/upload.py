# backend/app/api/routes/upload.py

import io
import re
import time
import zipfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from starlette.background import BackgroundTask

from backend.app.services.report_service import generate_pdf_report_from_docx


router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = Path("backend/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024
MAX_TEMP_FILE_AGE_SECONDS = 60 * 60


def make_safe_filename(filename: str) -> str:
    translit_map = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
        "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch",
        "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
    }

    original_path = Path(filename)
    name = original_path.stem
    ext = original_path.suffix.lower()

    transliterated = "".join(
        translit_map.get(char.lower(), char)
        for char in name
    )

    safe_name = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        transliterated,
    ).strip("_")

    if not safe_name:
        safe_name = "document"

    return f"{safe_name}{ext}"


def make_unique_path(directory: Path, filename: str) -> Path:
    path = directory / filename

    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1

    while True:
        candidate = directory / f"{stem}_{counter}{suffix}"

        if not candidate.exists():
            return candidate

        counter += 1


def delete_file(path: Path | str) -> None:
    file_path = Path(path)

    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
    except Exception as error:
        print(f"Не удалось удалить файл {file_path}: {error}")


def delete_files(paths: list[Path | str]) -> None:
    for path in paths:
        delete_file(path)


def cleanup_old_files(directory: Path) -> None:
    now = time.time()

    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue

        file_age = now - file_path.stat().st_mtime

        if file_age > MAX_TEMP_FILE_AGE_SECONDS:
            delete_file(file_path)


def get_safe_report_path(pdf_filename: str) -> Path:
    safe_name = Path(pdf_filename).name
    file_path = REPORT_DIR / safe_name
    return file_path


@router.post("/upload")
async def upload_docx(
    file: UploadFile = File(...),
    check_type: str = Form(...),
):
    cleanup_old_files(UPLOAD_DIR)
    cleanup_old_files(REPORT_DIR)

    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(
            status_code=400,
            detail="Only DOCX files are allowed",
        )

    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension",
        )

    safe_docx_name = make_safe_filename(file.filename)
    save_path = make_unique_path(
        UPLOAD_DIR,
        safe_docx_name,
    )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Файл слишком большой. Максимальный размер: 20 МБ",
        )

    with open(save_path, "wb") as buffer:
        buffer.write(contents)

    try:
        result = generate_pdf_report_from_docx(
            save_path,
            original_filename=file.filename,
            check_type=check_type,
        )
    except Exception as error:
        delete_file(save_path)

        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {error}",
        )

    delete_file(save_path)

    return {
        "message": "File uploaded and PDF report generated successfully",
        "original_filename": file.filename,
        "saved_filename": save_path.name,
        "pdf_report": result["report_filename"],
        "pdf_report_path": result["report_path"],
        "download_url": f"/download/{result['report_filename']}",
        "score": result["score"],
        "total_checks": result["total_checks"],
        "total_errors": result["total_errors"],
        "check_type": check_type,
        "error_categories": result.get("error_categories", []),
        "critical_errors_count": result.get("critical_errors_count", 0),
        "regular_errors_count": result.get("regular_errors_count", 0),
        "warnings_count": result.get("warnings_count", 0),
        "recommendations_count": result.get("recommendations_count", 0),
        "weighted_penalty": result.get("weighted_penalty", 0),
        "has_critical_errors": result.get("has_critical_errors", False),
        "status": result.get("status", "Соответствует требованиям"),
    }


@router.get("/download/{pdf_filename}")
async def download_pdf(
    pdf_filename: str,
):
    file_path = get_safe_report_path(
        pdf_filename
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF report not found",
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/pdf",
    )


@router.get("/download-zip")
async def download_reports_zip(
    files: str,
):
    file_names = [
        Path(file_name.strip()).name
        for file_name in files.split(",")
        if file_name.strip()
    ]

    if not file_names:
        raise HTTPException(
            status_code=400,
            detail="No PDF files selected",
        )

    file_paths = []

    for file_name in file_names:
        file_path = get_safe_report_path(file_name)

        if file_path.exists():
            file_paths.append(file_path)

    if not file_paths:
        raise HTTPException(
            status_code=404,
            detail="PDF reports not found",
        )

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_file:
        for file_path in file_paths:
            zip_file.write(
                file_path,
                arcname=file_path.name,
            )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=reports.zip",
        },
    )