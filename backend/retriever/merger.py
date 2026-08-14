def merge_results(raw_results: list[dict]) -> list[dict]:
    """
    Merges exact duplicate chunks retrieved across multiple sub-queries.
    If a chunk is found by multiple sub-queries, it keeps the highest retrieval score
    and tracks all sub-queries that found it.
    """
    merged_map = {}
    
    for item in raw_results:
        doc = item["document"]
        score = item["score"]
        source = item["source_query"]
        
        # Use page_content as a unique key for exact matches
        content = doc.page_content
        
        if content in merged_map:
            # Chunk was retrieved by multiple sub-queries
            merged_map[content]["score"] = max(merged_map[content]["score"], score)
            if source not in merged_map[content]["source_queries"]:
                merged_map[content]["source_queries"].append(source)
        else:
            merged_map[content] = {
                "document": doc,
                "score": score,
                "source_queries": [source]
            }
            
    return list(merged_map.values())
