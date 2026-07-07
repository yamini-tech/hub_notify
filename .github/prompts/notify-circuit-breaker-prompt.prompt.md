---
mode: agent
agent: notify-circuit-breaker
name: notify-circuit-breaker-prompt
description:
  Prompt for the notify-circuit-breaker agent. Generates circuit breaker logic with sliding window error monitoring, trip detection at configurable threshold, and Dead Letter Queue routing.
---

### Requirements

1.  **SQLAlchemy Model** — Create `app/models/circuit_breaker.py` with:
    - `CircuitBreakerState` table: `id` (PK), `channel` (unique), `is_tripped` (bool), `tripped_at` (datetime, nullable), `error_count` (int), `window_start` (datetime), `last_error_code` (str, nullable), `created_at`, `updated_at`
    - Create `app/models/__init__.py` importing all models

2.  **Sliding Window Monitor** — Create `app/queue/monitor.py` with:
    - `ChannelErrorMonitor` class using an in-memory deque per channel
    - `record(channel: str, success: bool)` — appends timestamped outcome, prunes entries older than `window_minutes`
    - `error_rate(channel: str) -> float` — ratio of failures to total in the window
    - `is_tripped(channel: str) -> bool` — true if error_rate > threshold and total count >= minimum_samples
    - Configurable `window_minutes` (default 5) and `threshold` (default 0.2)

3.  **Dead Letter Queue** — Create `app/queue/dlq.py` with:
    - `publish_to_dlq(payload: NotifyPayload, reason: str)` — publishes to `{channel}.dlq` queue with original payload + reason header
    - Declare DLQ queues as durable

4.  **Consumer Integration** — Modify `consumer.py:process_message()`:
    - On `dispatch()` success → `monitor.record(channel, success=True)`
    - On `dispatch()` exception → `monitor.record(channel, success=False)`; if `monitor.is_tripped(channel)`, call `publish_to_dlq()` instead of re-queueing
    - Log each trip event with channel name and current error rate

5.  **Alembic Migration** — Auto-generate migration for the new `circuit_breaker_state` table

### Constraints

- Python 3.11+, SQLAlchemy 2.x ORM style
- Monitor uses in-memory storage (no DB overhead for real-time error tracking)
- Circuit breaker state in DB is for observability/reporting only — the actual trip decision uses the in-memory monitor
- Existing error handling and retry logic must remain intact for non-tripped messages
- DLQ messages must preserve the original `NotifyPayload` for manual reprocessing

### Success Criteria

- `ruff check app/models/ app/queue/monitor.py app/queue/dlq.py` passes with no errors
- `monitor.error_rate()` returns accurate ratio within the sliding window
- When error_rate exceeds threshold, `is_tripped()` returns `True`
- Tripped messages land on `{channel}.dlq` queue instead of being retried
- Alembic migration creates the `circuit_breaker_state` table

### Usage Template

```
Generate circuit breaker logic for the notification service.

Create:
1. app/models/circuit_breaker.py with SQLAlchemy model
2. app/models/__init__.py
3. app/queue/monitor.py with sliding window error tracker
4. app/queue/dlq.py with Dead Letter Queue publisher
5. Modify app/queue/consumer.py to integrate monitoring
6. Alembic migration for the new table

Threshold: 20% failure over a 5-minute window.
Show all diffs and wait for my confirmation before applying.
```
