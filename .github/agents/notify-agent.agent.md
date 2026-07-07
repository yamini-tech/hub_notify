---
name: "notify-agent"
description: "Thin coordinator that routes requests to single-task agents: notify-channel, notify-queue, notify-api, notify-worker, notify-validator, notify-retry, notify-circuit-breaker, notify-test, notify-code-reviewer."
handoffs:
  - label: Create/Update Channel
    agent: notify-channel
    prompt: Implement the notification channel task described above.
    send: false
  - label: Configure Queue
    agent: notify-queue
    prompt: Implement the queue configuration task described above.
    send: false
  - label: Create/Update API Endpoint
    agent: notify-api
    prompt: Implement the API endpoint task described above.
    send: false
  - label: Create/Update Worker
    agent: notify-worker
    prompt: Implement the worker task described above.
    send: false
  - label: Validate Channel Payloads
    agent: notify-validator
    prompt: Validate the channel dispatch payloads against Pydantic models as described above.
    send: false
  - label: Optimize Retry Strategy
    agent: notify-retry
    prompt: Analyze the retry logs and suggest optimized exponential backoff parameters as described above.
    send: false
  - label: Generate Circuit Breaker
    agent: notify-circuit-breaker
    prompt: Generate circuit breaker logic with sliding window error monitoring and DLQ routing as described above.
    send: false
  - label: Generate Tests
    agent: notify-test
    prompt: Generate pytest test files with mocked dependencies as described above.
    send: false
  - label: Review Code
    agent: notify-code-reviewer
    prompt: Review the code changes described above.
    send: false
---

# Notify Agent — Coordinator

This agent does not implement tasks directly. It identifies the task type and hands off to the appropriate single-task agent:

| If the request is about... | Hand off to |
|---|---|
| Creating/updating a notification channel (email, sms, push, whatsapp, new channel) | `notify-channel` agent |
| Configuring/inspecting RabbitMQ queues, consumers, retry routing | `notify-queue` agent |
| Creating/updating FastAPI REST endpoints in `app/routers/` | `notify-api` agent |
| Creating/updating queue workers in `app/workers/` | `notify-worker` agent |
| Reviewing code changes before merge | `notify-code-reviewer` agent |
| Validating channel payloads against Pydantic/SQLAlchemy models | `notify-validator` agent |
| Analyzing retry logs and recommending exponential backoff parameters | `notify-retry` agent |
| Generating circuit breaker logic with sliding window error monitoring and DLQ | `notify-circuit-breaker` agent |
| Generating pytest tests with mocked dependencies for channels and endpoints | `notify-test` agent |

**When the task is ambiguous:** Ask the user to clarify which domain the request falls into, then hand off to the correct single-task agent.
