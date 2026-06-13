from pathlib import Path

from backend.app.services.report_service import (
    generate_pdf_report_from_docx
)

result = generate_pdf_report_from_docx(
    Path(
        "backend/uploads/3ce13935-e4e6-4bc9-b5e8-60df12049c03.docx"
    )
)

print(result)