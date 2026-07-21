---
name: notify-circuit-breaker
description: "Single-task agent for generating circuit breaker logic — tracks per-channel error rates over a sliding 5-minute window, trips at 20% failure threshold, and redirects to Dead Letter Queue. Does NOT handle channels, queues, retry config, or API endpoints."
---

# Notify Circuit Breaker Agent

Single task: Prevent cascading failures by monitoring per-channel error rates and tripping a circuit breaker when failures exceed 20% in a 5-minute sliding window.

## Scope

- `app/queue/consumer.py` — integrate error monitor into `process_message()`, NACK or DLQ on trip
- `app/models/circuit_breaker.py` — new SQLAlchemy model: `CircuitBreakerState(channel, is_tripped, tripped_at, error_count, window_start, last_error_code)`
- `app/queue/monitor.py` — new module: sliding 5-minute window error rate calculator
- `app/queue/dlq.py` — new module: Dead Letter Queue publisher per channel
- `alembic/` — migration for the new model

## Out of scope

This agent does NOT handle:
- Creating or updating channel implementations → use `notify-channel`
- RabbitMQ queue base configuration → use `notify-queue`
- Retry strategy or backoff parameters → use `notify-retry`
- Validating channel payloads against models → use `notify-validator`
- API endpoints → use `notify-api`
- Background workers → use `notify-worker`
- Review → use `notify-code-reviewer`

## Inputs

- `threshold` — optional custom failure rate percentage (default: 20%)
- `window_minutes` — optional custom sliding window size (default: 5)
- `dlq_enabled` — whether to route tripped messages to DLQ or NACK (default: true)

## Outputs

- `app/models/__init__.py` + `app/models/circuit_breaker.py` — SQLAlchemy model with fields: channel, is_tripped, tripped_at, error_count, window_start, last_error_code
- `app/queue/monitor.py` — `ChannelErrorMonitor` class: sliding window counter, `record(channel, success)`, `is_tripped(channel) -> bool`
- `app/queue/dlq.py` — `publish_to_dlq(payload, reason)` function
- Modified `consumer.py:process_message()` — on failure, feed error to monitor; if tripped, route to DLQ and log the trip
- Alembic migration script for `CircuitBreakerState` table

## Example prompts

- "Generate circuit breaker logic for the notification service. Create the model, monitor, and DLQ modules."
- "Add a sliding window error monitor to consumer.py that trips per channel at 20% failure."
- "Create a Dead Letter Queue publisher and integrate it into process_message for tripped channels."
- "Add an Alembic migration for the circuit_breaker_state table."
