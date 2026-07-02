---
mode: agent
agent: notify-rag
name: notify-rag-prompt
description:
  Prompt for the notify-rag agent. Creates or updates RAG pipeline components for document ingestion, chunking, embedding, and vector storage.
---

### Requirements

1.  **Document Ingestion:** Process incoming documents through receive → validate → extract text → chunk → embed → store pipeline.
2.  **Chunking:** Implement the specified chunking strategy (semantic, fixed-size, or recursive) with configurable parameters.
3.  **Embeddings:** Generate embeddings using the configured model (Ollama, OpenAI, or custom) with batching for efficiency.
4.  **Vector Storage:** Store embeddings in ChromaDB with proper collection management, metadata, and query support.

### Constraints

- Python 3.11+ with async/await for all I/O operations
- Embedding calls should be batched to avoid rate limits
- Chunk metadata must include source document ID, chunk index, and timestamps
- Vector collections must support hybrid (dense + metadata) search

### Success Criteria

- Documents are ingested through the full pipeline without data loss
- Chunks preserve document context and are independently retrievable
- Embeddings are generated and stored successfully
- Vector search returns relevant results with similarity scores
- `pytest -q` passes for the RAG pipeline tests

### Usage Template

```
Create/update the RAG ingestion pipeline to support [feature].
Include:
- [Chunking strategy] with [parameters]
- [Embedding model] integration
- [Vector store] collection setup
Show the diff and wait for my confirmation before applying.
```
