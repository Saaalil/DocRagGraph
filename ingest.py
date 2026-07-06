import os
import networkx as nx
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from config import get_embeddings, get_llm, CHROMA_DB_DIR, GRAPH_DB_PATH

def ingest_document(pdf_path: str):
    print(f"Loading document: {pdf_path}")
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    
    # 1. Vector Setup (Chroma)
    print("Chunking document for Vector Search...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    print("Initializing Embeddings Model (Qwen)...")
    embeddings = get_embeddings()
    
    print("Storing chunks in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    
    # 2. Graph Setup (NetworkX)
    print("Extracting Knowledge Graph Entities and Relationships (This may take a while)...")
    llm = get_llm(temperature=0)
    
    # Using LLMGraphTransformer to automatically extract graph properties
    llm_transformer = LLMGraphTransformer(llm=llm)
    
    # Extract graph documents from a subset of splits or all (warning: slow on CPU)
    # For large docs on CPU, you might want to slice `splits[:5]` for testing.
    graph_documents = llm_transformer.convert_to_graph_documents(splits)
    
    print("Building local NetworkX Graph...")
    G = nx.DiGraph()
    for doc in graph_documents:
        for node in doc.nodes:
            G.add_node(node.id, type=node.type)
        for rel in doc.relationships:
            G.add_edge(rel.source.id, rel.target.id, type=rel.type)
            
    # Save Graph to disk
    nx.write_graphml(G, GRAPH_DB_PATH)
    print(f"Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges saved to {GRAPH_DB_PATH}.")
    print("Ingestion Complete!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <path_to_pdf>")
    else:
        ingest_document(sys.argv[1])
