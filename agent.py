import os
import networkx as nx
from typing import Annotated, Literal
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from config import get_llm, get_embeddings, CHROMA_DB_DIR, GRAPH_DB_PATH

# 1. Load Stores
vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=get_embeddings()
)

try:
    graph_db = nx.read_graphml(GRAPH_DB_PATH)
except Exception as e:
    graph_db = nx.DiGraph()

# 2. Define Tools
@tool
def vector_search(query: str) -> str:
    """Use this tool to search for general information, context, or semantic similarity from the document."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])

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

# 3. Create Agent
llm = get_llm(temperature=0)
tools = [vector_search, graph_search]

# `create_react_agent` implements the ReAct loop (reasoning + acting) 
# It will loop until it has enough context to answer the user's question, fulfilling the "multiple tries" requirement.
system_prompt = (
    "You are an advanced Staff Data Scientist AI agent analyzing a document. "
    "You have access to a Hybrid GraphRAG system (Vector Database and Knowledge Graph). "
    "Use the `vector_search` tool to find semantic context. "
    "Use the `graph_search` tool to trace relationships and multi-hop connections between entities. "
    "If your initial search doesn't provide enough information, reformulate your query and try again. "
    "Provide a comprehensive, accurate final answer."
)

agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)

def query_agent(question: str):
    print("\n--- Agent Thinking ---")
    response = agent_executor.invoke({"messages": [("user", question)]})
    return response["messages"][-1].content
