---
name: notify-agent-skills
description: "Skills catalog for the hub_notify repository. Eleven single-task agents handle specific domains: MCP tools, RAG pipeline, plugin framework, AI workflow, monitoring, channel modules, queue configuration, API endpoints, workers, planning, and code review."
---

# Notify Agent — Skills Catalog

This document catalogs all single-task agents available for the `hub_notify` repository. Each agent handles exactly one task domain.

## Agents

### 1. notify-channel
- **File:** `notify-channel.agent.md` / Prompt: `notify-channel-prompt.prompt.md`
- **Single task:** Create or update a notification channel module (Email, SMS, Push, WhatsApp, or new provider)
- **Scope:** `app/channels/<channel>.py`, `app/config.py` (settings), dry-run support
- **Example prompt:** *"Create a Slack webhook channel following the pattern in app/channels/email.py."*

### 2. notify-queue
- **File:** `notify-queue.agent.md` / Prompt: `notify-queue-prompt.prompt.md`
- **Single task:** Configure or inspect RabbitMQ queues, exchanges, bindings, retry/dead-letter routing
- **Scope:** `app/queue/schemas.py`, `app/queue/producer.py`, `app/queue/consumer.py`, `app/queue/job_store.py`
- **Example prompt:** *"Add a slack.process queue with 3 retry attempts and dead-letter routing."*

### 3. notify-api
- **File:** `notify-api.agent.md` / Prompt: `notify-api-prompt.prompt.md`
- **Single task:** Create or update FastAPI REST endpoints
- **Scope:** `app/routers/notify.py`, `app/routers/jobs.py`, Pydantic request/response schemas
- **Example prompt:** *"Add a POST /api/v1/notify/send endpoint with recipient, channel, and message fields."*

### 4. notify-worker
- **File:** `notify-worker.agent.md` / Prompt: `notify-worker-prompt.prompt.md`
- **Single task:** Create or update background queue workers and register in `app/main.py` lifespan
- **Scope:** `app/workers/<name>_worker.py`, `app/workers/__init__.py`, `app/main.py`
- **Example prompt:** *"Create a Slack worker that consumes from slack.process and calls the Slack channel."*

### 5. notify-planner
- **File:** `notify-planner.agent.md`
- **Single task:** Generate implementation plans before any code work begins
- **Scope:** Read-only — produces Markdown plan documents only
- **Example prompt:** *"Plan adding a rate-limiting layer to the notify API endpoint."*

### 6. notify-code-reviewer
- **File:** `notify-code-reviewer.agent.md`
- **Single task:** Review code changes across correctness, readability, architecture, security, and performance
- **Scope:** Read-only — produces categorized review reports
- **Example prompt:** *"Review this PR for correctness and security before merge."*

### 7. notify-mcp
- **File:** `notify-mcp.agent.md` / Prompt: `notify-mcp-prompt.prompt.md`
- **Single task:** Create or update MCP server tools and configuration
- **Scope:** `mcp_hub_notify/`, `mcp-config.json`, `.vscode/mcp.json`
- **Example prompt:** *"Add a discoverDatabaseTables tool to the MCP server."*

### 8. notify-rag
- **File:** `notify-rag.agent.md` / Prompt: `notify-rag-prompt.prompt.md`
- **Single task:** Create or update RAG pipeline components (document ingestion, chunking, embeddings, vector storage)
- **Scope:** `app/workers/rag_worker.py`, `app/workers/file_worker.py`, ChromaDB, embedding services
- **Example prompt:** *"Update the RAG worker to use semantic chunking with overlap."*

### 9. notify-plugin
- **File:** `notify-plugin.agent.md` / Prompt: `notify-plugin-prompt.prompt.md`
- **Single task:** Create or update plugin framework components (metadata, hooks, rules, skills, agents)
- **Scope:** `plugin/` directory, plugin metadata, hook/rule/skill definitions
- **Example prompt:** *"Create a notify-audit plugin with a post-send hook."*

### 10. notify-ai-workflow
- **File:** `notify-ai-workflow.agent.md` / Prompt: `notify-ai-workflow-prompt.prompt.md`
- **Single task:** Create or update AI workflow orchestration pipelines using RabbitMQ queue chaining
- **Scope:** `app/queue/`, `app/workers/` (AI workers), `app/services/` (AI clients)
- **Example prompt:** *"Create a multi-stage AI workflow that ingests, analyzes, and enriches documents."*

### 11. notify-monitoring
- **File:** `notify-monitoring.agent.md` / Prompt: `notify-monitoring-prompt.prompt.md`
- **Single task:** Create or update notification monitoring, tracking, and observability features
- **Scope:** `app/workers/analytics_worker.py`, delivery tracking, metrics, alerting
- **Example prompt:** *"Add delivery confirmation tracking to the email channel."*

### Infrastructure Skills (reusable guides in `.github/skills/`)
- `notify-mcp` — MCP server tool creation and configuration
- `notify-rag` — RAG pipeline ingestion, chunking, embeddings, vector storage
- `notify-plugin` — Plugin framework creation (metadata, hooks, rules, skills, agents)
- `notify-ai-workflow` — AI workflow orchestration via RabbitMQ queue chaining
- `notify-monitoring` — Delivery tracking, metrics collection, alerting

## Safety policies (all agents)

- Never request or accept raw secrets in chat messages
- Never send production notifications without `CONFIRM_PROD_NOTIFICATION` token
- No direct production queue mutations without explicit human approval
- No automatic PR merging or repo-level approvals

## Maintenance notes

Keep `SKILLS.md` aligned with all `.agent.md` files, `.prompt.md` files, and `.github/skills/` files. When adding a new agent:
1. Create `<agent-name>.agent.md` in `.github/agents/`
2. Create `<agent-name>-prompt.prompt.md` in `.github/prompts/` (if the agent uses a prompt)
3. Create `.github/skills/<agent-name>/SKILL.md` (reusable skill guide)
4. Update this `SKILLS.md` catalog
5. Update `copilot-instructions.md` agent list
6. Update `notify-agent.agent.md` with handoff entry
7. Update `notify-prompt.prompt.md` with routing row
