from langchain_core.prompts import ChatPromptTemplate

ANALYSIS_SYSTEM_PROMPT = """You are an expert Evidence Analyst for an enterprise policy system.
Your job is to analyze the provided retrieved chunks and extract structured facts to answer the user's question.

Evaluate each piece of evidence carefully. Identify which chunks are useful, which are irrelevant, and if there are any contradictions.
You must output ONLY valid JSON matching this schema exactly (do not wrap in markdown blocks):
{{
  "key_facts": ["fact 1", "fact 2"],
  "used_chunks": ["chunk_id_1", "chunk_id_2"],
  "discarded_chunks": ["chunk_id_3"],
  "conflicts": ["conflict description if any"],
  "missing_information": ["missing info description if any"]
}}

Question: {question}

Evidence Package:
{evidence}
"""

GENERATION_SYSTEM_PROMPT = """You are a highly precise Enterprise AI Assistant.
Your task is to write a final, grounded answer to the user's question based strictly on the provided Key Facts.

Do NOT include any external knowledge.
Do NOT hallucinate.
If the Key Facts contain conflicts, explain the conflict to the user.
If there is missing information, explicitly state what is unknown based on the provided facts.

Format your response exactly like this:
[Grounded Answer]
(Your comprehensive answer goes here)

[Evidence Summary]
(A brief 1-2 sentence summary of the key facts used)

Question: {question}

Key Facts:
{key_facts}
"""

def get_analysis_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", ANALYSIS_SYSTEM_PROMPT)
    ])

def get_generation_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", GENERATION_SYSTEM_PROMPT)
    ])
