import fitz  # PyMuPDF
import os

def load_pdf(file_path):
    """Reads a PDF and extracts text page by page."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    doc = fitz.open(file_path)
    pages_data = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        pages_data.append({
            "page_number": page_num + 1,
            "text": text,
            "source": os.path.basename(file_path)
        })
        
    return pages_data
