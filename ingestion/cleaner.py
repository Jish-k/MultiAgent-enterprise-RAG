import re

def clean_text(text):
    """Cleans raw PDF text by removing extra spaces and normalizing formatting."""
    if not text:
        return ""
        
    # Remove excessive newlines (more than 2)
    cleaned = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing/leading whitespaces on each line
    cleaned = "\n".join([line.strip() for line in cleaned.split('\n')])
    
    # Fix broken words separated by newlines (e.g., standard- \n ization)
    cleaned = re.sub(r'-\n', '', cleaned)
    
    # Remove any weird invisible characters but preserve standard formatting
    cleaned = re.sub(r'[^\x00-\x7F\xA0-\xFF\u2013-\u2014\u2018-\u201D\u20B9]', '', cleaned)
    
    return cleaned.strip()

def clean_pages(pages_data):
    """Applies cleaning to a list of page dictionaries."""
    for page in pages_data:
        page["text"] = clean_text(page["text"])
    return pages_data
