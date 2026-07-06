import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()

# --- EMBEDDINGS CONFIGURATION ---
# Using Qwen 1.5B instruct for highly accurate local positional embeddings
EMBEDDING_MODEL_NAME = "Alibaba-NLP/gte-Qwen2-1.5B-instruct"

# We use sentence-transformers via HuggingFaceEmbeddings, which runs perfectly on CPU
# `trust_remote_code=True` is required for some modern models like Qwen embeddings.
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu', 'trust_remote_code': True},
        encode_kwargs={'normalize_embeddings': True}
    )

# --- LLM CONFIGURATION ---
# To provide the best experience on a 32GB RAM CPU, we fallback to local Ollama (qwen2.5)
# If a Together API key is present, we use their fast API to drastically speed up Graph Extraction.
def get_llm(temperature=0):
    together_api_key = os.getenv("TOGETHER_API_KEY")
    if together_api_key:
        print("Using Together AI API for high-speed LLM inference.")
        return ChatOpenAI(
            api_key=together_api_key,
            base_url="https://api.together.xyz/v1",
            model="Qwen/Qwen2.5-7B-Instruct-Turbo", # Excellent free tier model
            temperature=temperature
        )
    else:
        print("Using Local Ollama (qwen2.5) - CPU Inference (This may be slow for Graph indexing).")
        return ChatOllama(model="qwen2.5", temperature=temperature)

# --- STORAGE PATHS ---
CHROMA_DB_DIR = "./chroma_db"
GRAPH_DB_PATH = "./graph_db.graphml"
