from langchain_core.tools import tool
from database import graph_db

@tool
def graph_search(entity: str) -> str:
    """Use this tool to search for relationships and connected concepts in the knowledge graph. 
    Input should be a specific entity name (e.g., 'Company X', 'Machine Learning')."""
    if entity not in graph_db:
        # Fuzzy or partial matching fallback
        matches = [node for node in graph_db.nodes if entity.lower() in str(node).lower()]
        if not matches:
            return f"Entity '{entity}' not found in the graph."
        entity = matches[0]
        
    edges = list(graph_db.out_edges(entity, data=True)) + list(graph_db.in_edges(entity, data=True))
    if not edges:
        return f"No relationships found for '{entity}'."
        
    result = f"Relationships for {entity}:\n"
    for u, v, data in edges:
        rel_type = data.get("type", "related to")
        result += f"- {u} is {rel_type} {v}\n"
    return result
