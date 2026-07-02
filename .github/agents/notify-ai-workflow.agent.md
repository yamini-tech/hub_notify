---
name: notify-ai-workflow
description: "Single-task agent for creating and updating AI workflow orchestration pipelines using RabbitMQ queue chaining. Does NOT handle channels, individual queues, API endpoints, or standalone workers."
---

# Notify AI Workflow Agent

Single task: Create or update AI workflow orchestration pipelines that chain multiple RabbitMQ queues and workers into coordinated AI processing flows.

## Scope

- `app/queue/` — workflow queue definitions, routing topology for AI pipelines
- `app/workers/` — AI-specific workers (AI worker, embedding worker, memory worker)
- `app/services/` — AI service integrations (AI client, backend client)
- Workflow pipeline definitions (step sequencing, data passing between queues)
- Queue chaining for multi-stage AI processing (ingest → process → enrich → store)

## Out of scope

This agent does NOT handle:
- Notification channel implementations → use `notify-channel`
- Individual queue configuration (retry, DLQ) → use `notify-queue`
- HTTP API endpoints → use `notify-api`
- Standalone worker creation → use `notify-worker`
- Planning or review → use `notify-planner` or `notify-code-reviewer`

## Inputs

- `workflow_name` — the AI workflow name (e.g., `document_enrichment`, `content_analysis`)
- `pipeline_steps` — ordered list of processing stages (e.g., `extract → analyze → enrich → store`)
- `queue_topology` — queue names and routing between stages
- `ai_model` — the model or service to use for AI processing

## Outputs

- New or updated workflow pipeline definitions in `app/queue/` and `app/workers/`
- Queue chaining configuration (producer → consumer → next producer pattern)
- AI service integration code in `app/services/`
- `pytest` command to verify the workflow pipeline

## Example prompts

- "Create a multi-stage AI workflow that ingests documents, extracts entities, enriches with external data, and stores results."
- "Add a content moderation step between the ingestion and storage stages in the AI pipeline."
- "Update the AI workflow to route failed enrichments to a manual review queue."

## Related Skills

- `.github/skills/notify-ai-workflow/SKILL.md` — detailed workflows for queue chaining, multi-stage AI pipelines, and AI service integration
