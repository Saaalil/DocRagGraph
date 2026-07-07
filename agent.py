import os
from langgraph.prebuilt import create_react_agent
from config import get_llm
from skills import vector_search, graph_search

# 1. Create Agent
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
