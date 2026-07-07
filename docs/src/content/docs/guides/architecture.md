---
title: System Architecture & Workflow
description: A deep dive into how the Hybrid GraphRAG system operates behind the scenes.
---

This page explains exactly how **DocRagGraph** processes your documents and answers your questions. We've designed this breakdown so that anyone—from a software engineer to a business executive—can understand the massive value of the system.

## The Ingestion Phase: Reading the Document

Before you can ask a question, the system must "read" your PDF. But it doesn't just scan the text; it builds a dual-layer brain.

1. **Chunking (The Librarian):** The document is sliced into small paragraphs. A local AI model (`Alibaba-NLP/gte-Qwen2-1.5B-instruct`) converts these paragraphs into numbers (vectors) and stores them in **ChromaDB**. This allows the system to instantly find paragraphs that mean the same thing as your question.
2. **Graph Extraction (The Detective):** A powerful Language Model slowly reads every single page. Every time it spots an Entity (a person, a company, a law), it draws a node. Every time it spots a connection (Company A *owns* Company B), it draws a line. This web of connections is saved in **NetworkX**.

---

## The Query Phase: The Autonomous Agent

When you type a question, it is handed off to a **LangGraph ReAct Agent**. "ReAct" stands for Reasoning and Acting. 

Instead of a standard script that just pulls data and spits out an answer, the Agent has free will. It operates in a continuous loop:

<div class="mermaid">
graph TD
    A[👤 Complex User Query] --> B{🤖 LangGraph Agent}
    
    B -->|Requires Semantic Context| C[(Chroma Vector DB)]
    B -->|Requires Deep Relationships| D[(NetworkX Graph DB)]
    
    C -.->|Returns Text Chunks| E[🧠 Self-Reflection]
    D -.->|Returns Multi-Hop Paths| E
    
    E -->|Information Missing| B
    E -->|Confident in Answer| F[✅ Highly Accurate Output]
    
    style B fill:#d29d72,stroke:#110f0e,stroke-width:2px,color:#110f0e
    style F fill:#f0c39f,stroke:#110f0e,stroke-width:2px,color:#110f0e
    style E fill:#3a2b20,stroke:#110f0e,stroke-width:2px,color:#e8e3d9
</div>

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'dark' });
  mermaid.init(undefined, document.querySelectorAll('.mermaid'));
</script>

### 1. The Decision
The Agent asks itself: *"Does this question require me to find a specific fact, or do I need to connect the dots across multiple entities?"* It then triggers the appropriate database.

### 2. The Retrieval
If it needs the Graph, it starts at one node (e.g., "The Supplier") and walks along the connected lines to find out what the supplier is responsible for, who they report to, and what happens if they fail. 

### 3. The Reflection Loop
This is where the magic happens. The Agent reads the data it just retrieved. If it realizes, *"Wait, I found out who the supplier is, but I still don't know the late fee penalty"*, it will **automatically loop back** and query the Vector Database for the penalty clause. 

It only stops and presents the final answer to you when it is 100% confident it has gathered all the pieces of the puzzle. 

## The Result
You get an answer that is highly accurate, contextually aware, and deeply reasoned—something that traditional RAG systems simply cannot achieve.
