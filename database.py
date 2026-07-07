import networkx as nx
from langchain_chroma import Chroma
from config import get_embeddings, CHROMA_DB_DIR, GRAPH_DB_PATH

# 1. Load Stores
vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=get_embeddings()
)

try:
    graph_db = nx.read_graphml(GRAPH_DB_PATH)
except Exception as e:
    graph_db = nx.DiGraph()
