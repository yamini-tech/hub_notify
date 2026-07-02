---
mode: agent
agent: notify-ai-workflow
name: notify-ai-workflow-prompt
description:
  Prompt for the notify-ai-workflow agent. Creates or updates AI workflow orchestration pipelines using RabbitMQ queue chaining.
---

### Requirements

1.  **Pipeline Definition:** Define multi-stage AI workflows as ordered steps, each consuming from and publishing to specific queues.
2.  **Queue Chaining:** Implement the producer → consumer → next producer pattern so each stage passes results to the next.
3.  **AI Integration:** Connect workflow stages to AI services (Ollama, OpenAI, or custom) through `app/services/` clients.
4.  **Error Handling:** Each stage must handle failures independently — failed items route to a dead-letter or review queue without blocking the pipeline.

### Constraints

- Python 3.11+ with async/await and aio-pika for RabbitMQ
- Each pipeline stage is an independent queue consumer that publishes to the next stage's queue
- Workflow state tracked in message headers or payload (not external state store)
- Stages must be independently deployable and testable

### Success Criteria

- Pipeline processes end-to-end through all defined stages
- Each stage correctly receives input from the previous queue and publishes to the next
- Failed stages do not block downstream processing
- Pipeline can be monitored via queue depth and consumer status
- `pytest -q` passes for workflow integration tests

### Usage Template

```
Create an AI workflow pipeline [name] with stages:
- Stage 1: [name] — consumes from [queue], publishes to [queue]
- Stage 2: [name] — consumes from [queue], publishes to [queue]
- Stage 3: [name] — consumes from [queue], stores final result
Include AI integration via [service/client] and error handling per stage.
Show the diff and wait for my confirmation before applying.
```
