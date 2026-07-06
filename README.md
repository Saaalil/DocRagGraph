# Agentic GraphRAG System

An advanced, agentic Hybrid GraphRAG system designed to extract and retrieve information from documents using a combination of vector search and knowledge graphs. Built for high accuracy and deep, multi-hop reasoning over complex text.

## Architecture Overview

This project implements a dual-retrieval pipeline managed by a stateful agentic loop:

1. **Vector Retrieval**: Uses `ChromaDB` to store and retrieve semantic chunks. Embeddings are generated locally using the `Alibaba-NLP/gte-Qwen2-1.5B-instruct` model via `sentence-transformers`.
2. **Graph Retrieval**: Uses an LLM to extract entities and relationships, storing them in a local `NetworkX` graph. This enables multi-hop reasoning across connected concepts.
3. **Agentic Loop**: Utilizes `LangGraph` (specifically a ReAct agent) to dynamically route queries between the Vector Database and the Knowledge Graph. If the initial retrieved context is insufficient, the agent self-reflects, reformulates its query, and loops until a satisfactory answer is formed.

## Prerequisites

- Python 3.9 or higher
- 32GB RAM recommended for CPU-only environments.

## Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <your-repo-url>
cd DocRag
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

By default, the system is configured to use local CPU inference.

### Local LLM via Ollama
If running purely locally, ensure you have [Ollama](https://ollama.com/) installed and the Qwen 2.5 model pulled:
```bash
ollama pull qwen2.5
```
*Note: Extracting the knowledge graph purely on a CPU via a local LLM can be extremely time-consuming.*

### High-Speed API (Recommended for Graph Indexing)
To significantly accelerate the knowledge graph extraction phase, you can use a free-tier API such as Together AI. 
Create a `.env` file in the root directory and add your API key:
```ini
TOGETHER_API_KEY=your_api_key_here
```
When this key is present, the system will automatically switch to the remote API for LLM inference while keeping vector embeddings strictly local.

## Usage

### 1. Ingesting a Document
To parse a PDF, chunk the text, generate embeddings, and build the knowledge graph, run the ingestion script:

```bash
python ingest.py "path/to/your/document.pdf"
```
This process will create a `chroma_db` directory for the vectors and a `graph_db.graphml` file for the knowledge graph.

### 2. Querying the System
Once the document is ingested, start the agentic chat interface:

```bash
python main.py
```
Type your questions into the prompt. The LangGraph agent will output its reasoning process as it searches the vector database and the knowledge graph to synthesize the final answer. Type `exit` or `quit` to terminate the session.

## License

This project is licensed under the MIT License.
