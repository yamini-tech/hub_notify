---
name: notify-ai-workflow
description: Create or update AI workflow orchestration pipelines that chain multiple RabbitMQ queues into coordinated multi-stage AI processing flows. Use when building document enrichment, content analysis, or any pipeline that passes data through sequential AI processing stages.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 01 Jul 2026 00:00:00 GMT
---

# Notify AI Workflow Skill

## Contents
- [Core Guidelines](#core-guidelines)
- [Workflow: Building a Multi-Stage AI Pipeline](#workflow-building-a-multi-stage-ai-pipeline)
- [Workflow: Adding a Stage to an Existing Workflow](#workflow-adding-a-stage-to-an-existing-workflow)
- [Examples](#examples)

## Core Guidelines

- **Queue Chaining Pattern**: Each pipeline stage is an independent queue consumer that processes messages and publishes results to the next stage's queue. Stages never call each other directly — they communicate only through queues.
- **Stage Isolation**: Each stage must handle failures independently. A failure in stage 2 must not block stage 1 or stage 3. Failed items route to a dead-letter or manual-review queue specific to that stage.
- **Data Passing**: Workflow state (document ID, source metadata, processing history) travels in message headers or payload. Never use external state storage for workflow progression — the message is the source of truth.
- **Idempotent Stages**: Each stage should be idempotent when possible. If a message is re-delivered (e.g., after a consumer crash), re-processing should produce the same result or safely skip already-processed items.
- **Observability**: Every stage must log: received message count, processing duration, success/failure count, and next stage routing. Use structured logging with correlation IDs that span the entire workflow.

## Workflow: Building a Multi-Stage AI Pipeline

Use this checklist to create a new AI workflow orchestration pipeline.

**Task Progress:**
- [ ] 1. Define the pipeline stages and the data flow between them (what each stage produces and the next stage consumes).
- [ ] 2. Create the RabbitMQ queues for each stage with naming convention `<workflow>.<stage>`.
- [ ] 3. Implement each stage as a queue consumer that processes messages and publishes to the next queue.
- [ ] 4. Wire up AI service integration in `app/services/` for stages that need AI processing.
- [ ] 5. Implement error handling per stage — dead-letter routing for unrecoverable failures, retry queues for transient failures.
- [ ] 6. Register all consumers in `app/main.py` lifespan for startup.
- [ ] 7. Write end-to-end tests that verify the full pipeline processes a message through all stages.
- [ ] 8. **Feedback Loop**: Submit a test message -> trace through each stage's logs -> verify data integrity across stages -> fix routing or processing errors -> re-test.

1. **Define Stages**: Map out the pipeline as a series of discrete processing steps. Example: `ingest → classify → enrich → notify`. Each step has a clear input, processing logic, and output.

2. **Create Queue Topology**: Define queues for each stage plus retry and dead-letter variants:
   - `<workflow>.<stage>.process` — main processing queue
   - `<workflow>.<stage>.retry` — retry queue with TTL
   - `<workflow>.<stage>.failed` — dead-letter queue

3. **Implement Consumers**: Each consumer subscribes to its `.process` queue, does work, and publishes the result to the next stage's `.process` queue. The last stage stores the final result or sends a notification.

4. **Wire AI Services**: Create service clients in `app/services/` for AI model access. Use dependency injection so stages can be tested with mock AI services.

5. **Add Error Boundaries**: Wrap each stage's processing in try/except. On transient errors (timeout, rate limit), nack with requeue or route to retry. On permanent errors (invalid input, schema violation), route to dead-letter.

6. **Register Lifespan**: Add each consumer's `start()` and `stop()` to `app/main.py` lifespan. Ensure graceful shutdown completes in-flight processing.

## Workflow: Adding a Stage to an Existing Workflow

Use this checklist when inserting a new processing stage into an existing pipeline.

**Task Progress:**
- [ ] 1. Identify where the new stage fits in the pipeline (between which two existing stages).
- [ ] 2. Create the queue for the new stage: `<workflow>.<new_stage>.process`.
- [ ] 3. Update the preceding stage's producer to publish to the new stage's queue instead of the original next stage.
- [ ] 4. Implement the new stage consumer that processes messages and publishes to the original next stage.
- [ ] 5. Add retry and dead-letter queues for the new stage.
- [ ] 6. Update pipeline documentation and stage sequence.

## Examples

### High-Fidelity Implementation: Embedding → AI → Memory Pipeline

**Stage 1 — Embedding Worker (`app/workers/embedding_worker.py`):**
```python
from app.queue.schemas import Job, JobType
from app.queue.producer import publish_job

async def _process(job: Job) -> None:
    next_job = Job(
        job_type=JobType.AI_ORCHESTRATION,
        queue="ai.orchestration",
        label="AI orchestration",
        payload=job.payload,
    )
    await publish_job(next_job)
```

**Stage 2 — AI Orchestration Worker (`app/workers/ai_worker.py`):**
```python
from app.queue.schemas import Job, JobType
from app.queue.producer import publish_job

async def _process(job: Job) -> None:
    next_job = Job(
        job_type=JobType.MEMORY_PROCESSING,
        queue="memory.processing",
        label="Memory processing",
        payload=job.payload,
    )
    await publish_job(next_job)
```

**Stage 3 — Memory Worker (`app/workers/memory_worker.py`):**
```python
from app.queue.schemas import Job

async def _process(job: Job) -> None:
    logger.info("Pipeline completed for job %s", job.job_id)
```

**Registration in `app/main.py`:**
```python
from app.workers import (
    embedding_worker,
    ai_worker,
    memory_worker,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_queues()
    workers = [
        embedding_worker.run,
        ai_worker.run,
        memory_worker.run,
    ]
    tasks = [asyncio.create_task(w()) for w in workers]
    yield
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
```
