from datasets import load_dataset

def load_hotpotqa(subset_size=100, split="validation"):
    """
    Loads a subset of the HotpotQA dataset and extracts the context paragraphs.
    Converts them into the internal document format (similar to load_pdf).
    """
    print(f"Loading {subset_size} samples from HotpotQA ({split} split)...")
    dataset = load_dataset('hotpotqa/hotpot_qa', 'fullwiki', split=split)
    
    # We only take the first `subset_size` questions
    subset = dataset.select(range(min(subset_size, len(dataset))))
    
    pages_data = []
    seen_titles = set()
    
    for item in subset:
        context = item.get("context", {})
        titles = context.get("title", [])
        sentences_list = context.get("sentences", [])
        
        for title, sentences in zip(titles, sentences_list):
            if title in seen_titles:
                continue
            
            seen_titles.add(title)
            
            # Combine sentences into a single paragraph text
            text = " ".join(sentences)
            
            pages_data.append({
                "page_number": 1,
                "text": text,
                "source": title
            })
            
    print(f"Extracted {len(pages_data)} unique context documents from HotpotQA.")
    return pages_data
