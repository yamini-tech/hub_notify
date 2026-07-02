---
name: notify-rag
description: Create or update RAG (Retrieval-Augmented Generation) pipeline components including document ingestion, chunking strategies, embedding generation, and ChromaDB vector storage. Use when building or modifying AI-powered document search or knowledge retrieval features.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 01 Jul 2026 00:00:00 GMT
---

# Notify RAG Skill

## Contents
- [Core Guidelines](#core-guidelines)
- [Workflow: Setting Up a RAG Ingestion Pipeline](#workflow-setting-up-a-rag-ingestion-pipeline)
- [Workflow: Integrating a New Document Type](#workflow-integrating-a-new-document-type)
- [Examples](#examples)

## Core Guidelines

- **Pipeline Stages**: Every RAG ingestion pipeline follows a strict order: receive → validate → extract text → chunk → embed → store. Never skip stages. Each stage must be independently testable.
- **Chunking Strategy**: Choose the strategy based on document type — semantic chunking for prose/narrative, fixed-size for structured data, recursive for mixed content. Always preserve source metadata (document ID, chunk index, page number) in each chunk.
- **Embedding Batching**: Send embeddings to the model in batches (default: 10) to avoid rate limits and memory pressure. Log batch progress and handle partial failures (retry individual embeddings, not the whole batch).
- **Vector Store Isolation**: Use separate ChromaDB collections for different document types or tenants. Never mix unrelated document embeddings in the same collection. Store metadata alongside vectors for filtered search.
- **Async I/O**: All pipeline operations (file reads, API calls, database writes) must use async/await. Use asyncio.gather for parallel operations where order doesn't matter.

## Workflow: Setting Up a RAG Ingestion Pipeline

Use this checklist to implement or modify the document ingestion pipeline.

**Task Progress:**
- [ ] 1. Define the document source and format (file upload, API webhook, queue consumer).
- [ ] 2. Implement text extraction for the document format (plain text, PDF, Markdown, HTML).
- [ ] 3. Choose and configure the chunking strategy with appropriate parameters (chunk size, overlap).
- [ ] 4. Configure the embedding model connection (Ollama endpoint, model name, batch size).
- [ ] 5. Set up the ChromaDB collection with the correct embedding dimension and metadata schema.
- [ ] 6. Implement the pipeline orchestration in `app/workers/rag_worker.py`.
- [ ] 7. Add progress tracking and error handling for each pipeline stage.
- [ ] 8. **Feedback Loop**: Test with a sample document -> review chunk quality and embedding accuracy -> adjust chunking parameters or model selection -> re-run.

1. **Define Source**: Determine how documents enter the pipeline. For file uploads, use the file worker. For API-triggered ingestion, use a queue message with document metadata.
2. **Resolve Storage Path**: Combine `settings.upload_dir` with the document's `storage_path` to get the absolute file path. Log the resolved path for debugging.
3. **Delegate to AI Service**: Call `ai_client.ingest_document()` with document metadata — the external AI service handles text extraction, chunking, embedding, and vector storage.
4. **Update Job Progress**: Use `job_store.update()` to report progress (10% received, 50% processing, 100% done) and status messages at each stage.
5. **Notify Backend**: Call `backend_client.mark_document_processed()` to inform the backend service that indexing is complete.
6. **Handle Errors**: Wrap processing in try/except and let exceptions propagate to the RabbitMQ worker's built-in retry/dead-letter logic.

## Workflow: Integrating a New Document Type

Use this checklist when adding support for a new document format in the RAG pipeline.

**Task Progress:**
- [ ] 1. Determine the document type and its storage path format.
- [ ] 2. Verify the AI service supports the new document type for text extraction and chunking.
- [ ] 3. Update `rag_worker.py` to pass the correct `file_type` parameter to `ai_client.ingest_document()`.
- [ ] 4. Ensure the file worker routes the document to the `rag.bulk_ingest` queue.
- [ ] 5. Test end-to-end: upload document → worker processes → job marked done.

## Examples

### High-Fidelity Implementation: Document Ingestion via AI Service

**RAG Worker (`app/workers/rag_worker.py`):**
```python
from app.services.ai_client import ai_client
from app.services.backend_client import backend_client
from app.queue.job_store import job_store
from app.queue.schemas import Job, JobStatus
from app.config import settings
from pathlib import Path

async def _process(job: Job) -> None:
    payload = job.payload
    document_id = payload["document_id"]
    storage_path = payload["storage_path"]
    file_type = payload["file_type"]
    filename = payload["filename"]
    absolute_path = str(Path(settings.upload_dir) / storage_path)

    await job_store.update(
        job.job_id, JobStatus.PROCESSING,
        progress=10, message=f"Received {filename}",
    )

    result = await ai_client.ingest_document(
        document_id=document_id,
        user_id=payload["user_id"],
        storage_path=absolute_path,
        file_type=file_type,
        filename=filename,
    )

    try:
        await backend_client.mark_document_processed(document_id=document_id)
    except Exception:
        logger.exception("Could not update backend document status.")

    await job_store.update(
        job.job_id, JobStatus.DONE,
        progress=100, message="Document indexed successfully.",
    )
```

**AI Client (`app/services/ai_client.py`):**
```python
import httpx
from app.config import settings

AI_SERVICE_URL = settings.ai_service_url

class AIClient:
    async def ingest_document(
        self, document_id: str, user_id: str,
        storage_path: str, file_type: str, filename: str,
    ):
        payload = {
            "document_id": document_id,
            "user_id": user_id,
            "file_path": storage_path,
            "file_type": file_type,
            "filename": filename,
        }
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/api/v1/rag/ingest",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            logger.info("Stored %d chunks.", result["chunks_stored"])
            return result

ai_client = AIClient()
```
