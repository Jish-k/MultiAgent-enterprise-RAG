from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_documents(pages_data, chunk_size=1000, chunk_overlap=200):
    """Splits enriched pages into semantic chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    documents = []
    for page in pages_data:
        if not page["text"].strip():
            continue
            
        chunks = splitter.split_text(page["text"])
        
        for chunk in chunks:
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": page["source"],
                    "page_number": page["page_number"],
                    "section": page.get("section_title", "Unknown")
                }
            )
            documents.append(doc)
            
    return documents
