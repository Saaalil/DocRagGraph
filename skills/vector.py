from langchain_core.tools import tool
from database import vectorstore

@tool
def vector_search(query: str) -> str:
    """Use this tool to search for general information, context, or semantic similarity from the document."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])
