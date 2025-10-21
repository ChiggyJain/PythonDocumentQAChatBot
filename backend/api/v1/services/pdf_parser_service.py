
import fitz 
from pathlib import Path
from typing import Tuple, Dict, Any

def parse_pdf(file_path: Path) -> Dict[str, Any]:
    """
    Parse a PDF file and return its full text content along with basic metadata.
    Args:
        file_path (Path): Path to the PDF file.
    Returns:
        Tuple[str, dict]: 
            - Extracted text from all pages
            - Metadata dictionary (filename, page_count)
    Raises:
        ValueError: If PDF is empty or cannot be read.
    """
    print(f"parse_pdf file_path: {file_path}\n")
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}") 
    totalPageCount = 0
    all_pages = []
    try:
        with fitz.open(file_path) as pdf:
            totalPageCount = pdf.page_count
            if totalPageCount == 0:
                raise ValueError("PDF has no pages.")
            for page_number, page in enumerate(pdf, start=1):
                if page.get_text().strip():
                    all_pages.append({
                        "pageNo": page_number,
                        "pageContent": page.get_text().strip()
                    })
        result = {
            "overallPdfSummary": {
                "filePath": str(file_path.resolve()),
                "fileName": file_path.name,
                "fileExtension": file_path.suffix,
                "totalPageCount": totalPageCount
            },
            "allPagesDetails": all_pages
        }
        return result
    except Exception as e:
        raise ValueError(f"parse_pdf failed to parse PDF: {str(e)}")
