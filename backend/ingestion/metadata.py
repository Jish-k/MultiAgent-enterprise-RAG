import re

def extract_metadata(pages_data):
    """Enriches pages with section titles based on heuristics."""
    current_section = "General"
    
    for page in pages_data:
        text = page["text"]
        
        # Heuristic: Look for lines that look like headers (e.g., "1. Introduction" or short bold lines)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Simple heuristic for section headers: Starts with a number, or short title
            if re.match(r'^\d+\.\s+[A-Z]', line) and len(line) < 80:
                current_section = line
                break
            elif line.isupper() and 3 < len(line) < 50:
                current_section = line.title()
                break
                
        page["section_title"] = current_section
        
    return pages_data
